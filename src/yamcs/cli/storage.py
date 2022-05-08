import os
import shutil
import sys
import tempfile

from yamcs.cli import utils
from yamcs.client import YamcsClient
from yamcs.core.helpers import to_isostring


def _parse_ys_url(url):
    parts = url[5:].split("/", 1)
    if len(parts) == 2 and parts[1]:
        return parts[0], parts[1]
    else:
        return parts[0], None


class StorageCommand(utils.Command):
    def __init__(self, parent):
        super(StorageCommand, self).__init__(parent, "storage", "Manage object storage")

        subparsers = self.parser.add_subparsers(title="Commands", metavar="COMMAND")
        subparsers.required = True

        subparser = self.create_subparser(subparsers, "ls", "List buckets or objects")
        subparser.add_argument(
            "bucket", metavar="BUCKET", type=str, nargs="?", help="bucket or object"
        )
        subparser.add_argument(
            "-l", dest="long", action="store_true", help="List in long format"
        )
        subparser.add_argument(
            "-r", "-R", dest="recurse", action="store_true", help="List recursively"
        )
        subparser.set_defaults(func=self.ls)

        subparser = self.create_subparser(subparsers, "list", "Synonym for ls")
        subparser.add_argument(
            "bucket", metavar="BUCKET", type=str, nargs="?", help="bucket or object"
        )
        subparser.add_argument(
            "-l", dest="long", action="store_true", help="List in long format"
        )
        subparser.add_argument(
            "-r", "-R", dest="recurse", action="store_true", help="List recursively"
        )
        subparser.set_defaults(func=self.ls)

        subparser = self.create_subparser(subparsers, "mb", "Make buckets")
        subparser.add_argument(
            "bucket", metavar="BUCKET", type=str, nargs="+", help="bucket"
        )
        subparser.set_defaults(func=self.mb)

        subparser = self.create_subparser(subparsers, "rb", "Remove buckets")
        subparser.add_argument(
            "bucket", metavar="BUCKET", type=str, nargs="+", help="bucket"
        )
        subparser.set_defaults(func=self.rb)

        subparser = self.create_subparser(
            subparsers, "cat", "Concatenate object content to stdout"
        )
        subparser.add_argument(
            "object",
            metavar="OBJECT",
            type=str,
            nargs="+",
            help="object in the format ys://bucket/object",
        )
        subparser.set_defaults(func=self.cat)

        subparser = self.create_subparser(subparsers, "cp", "Copy files or objects")
        subparser.add_argument(
            "src",
            metavar="SRC",
            type=str,
            help="object in the format ys://bucket/object",
        )
        subparser.add_argument(
            "dst",
            metavar="DST",
            type=str,
            help="object in the format ys://bucket/object",
        )
        subparser.set_defaults(func=self.cp)

        subparser = self.create_subparser(subparsers, "mv", "Move files or objects")
        subparser.add_argument(
            "src",
            metavar="SRC",
            type=str,
            help="object in the format ys://bucket/object",
        )
        subparser.add_argument(
            "dst",
            metavar="DST",
            type=str,
            help="object in the format ys://bucket/object",
        )
        subparser.set_defaults(func=self.mv)

        subparser = self.create_subparser(subparsers, "rm", "Remove objects")
        subparser.add_argument(
            "object",
            metavar="OBJECT",
            type=str,
            nargs="+",
            help="object in the format ys://bucket/object",
        )
        subparser.set_defaults(func=self.rm)

    def ls(self, args):
        opts = utils.CommandOptions(args)
        client = YamcsClient(**opts.client_kwargs)
        storage = client.get_storage_client()

        if args.bucket:
            if args.bucket.startswith("ys://"):
                bucket_name, prefix = _parse_ys_url(args.bucket)
            else:
                bucket_name = args.bucket
                prefix = None

            delimiter = "/"
            if args.recurse:
                delimiter = None

            listing = storage.list_objects(
                bucket_name=bucket_name, delimiter=delimiter, prefix=prefix
            )
            rows = []
            for prefix in listing.prefixes:
                url = "ys://{}/{}".format(bucket_name, prefix)
                if args.long:
                    rows.append(["0", "", url])
                else:
                    rows.append([url])

            for obj in listing.objects:
                url = "ys://{}/{}".format(bucket_name, obj.name)
                if args.long:
                    rows.append([str(obj.size), to_isostring(obj.created), url])
                else:
                    rows.append([url])

            utils.print_table(rows)
        else:
            for bucket in storage.list_buckets():
                print("ys://{}/".format(bucket.name))

    def mb(self, args):
        opts = utils.CommandOptions(args)
        client = YamcsClient(**opts.client_kwargs)
        storage = client.get_storage_client()

        for bucket in args.bucket:
            storage.create_bucket(bucket_name=bucket)

    def rb(self, args):
        opts = utils.CommandOptions(args)
        client = YamcsClient(**opts.client_kwargs)
        storage = client.get_storage_client()

        for bucket in args.bucket:
            storage.remove_bucket(bucket_name=bucket)

    def rm(self, args):
        opts = utils.CommandOptions(args)
        client = YamcsClient(**opts.client_kwargs)
        storage = client.get_storage_client()

        for obj in args.object:
            if not obj.startswith("ys://"):
                print("*** specify objects in the format ys://bucket/object")
                return False

            bucket_name, object_name = _parse_ys_url(obj)
            if not object_name:
                print("*** specify objects in the format ys://bucket/object")
                return False

            storage.remove_object(bucket_name=bucket_name, object_name=object_name)

    def cat(self, args):
        opts = utils.CommandOptions(args)
        client = YamcsClient(**opts.client_kwargs)
        storage = client.get_storage_client()

        for obj in args.object:
            if not obj.startswith("ys://"):
                print("*** specify objects in the format ys://bucket/object")
                return False

            bucket_name, object_name = _parse_ys_url(obj)
            if not object_name:
                print("*** specify objects in the format ys://bucket/object")
                return False

            content = storage.download_object(
                bucket_name=bucket_name, object_name=object_name
            )
            sys.stdout.buffer.write(content)

    def mv(self, args):
        opts = utils.CommandOptions(args)
        client = YamcsClient(**opts.client_kwargs)
        storage = client.get_storage_client()

        if self.cp(args) is not False:
            if args.src.startswith("ys://"):
                bucket_name, object_name = _parse_ys_url(args.src)
                if not object_name:
                    print("*** specify objects in the format ys://bucket/object")
                    return False

                storage.remove_object(bucket_name=bucket_name, object_name=object_name)
            else:
                os.remove(args.src)

    def cp(self, args):
        opts = utils.CommandOptions(args)
        if args.src.startswith("ys://"):
            if args.dst.startswith("ys://"):
                return self._cp_object_to_object(opts, args.src, args.dst)
            else:
                return self._cp_object_to_file(opts, args.src, args.dst)
        else:
            if args.dst.startswith("ys://"):
                return self._cp_file_to_object(opts, args.src, args.dst)
            else:
                shutil.copy(args.src, args.dst)

    def _cp_object_to_object(self, opts, src, dst):
        fd, path = tempfile.mkstemp()
        try:
            self._cp_object_to_file(opts, src, path)
            self._cp_file_to_object(opts, path, dst)
        finally:
            os.close(fd)
            os.remove(path)

    def _cp_object_to_file(self, opts, src, dst):
        src_bucket, src_object = _parse_ys_url(src)
        _, src_filename = os.path.split(src_object)

        client = YamcsClient(**opts.client_kwargs)
        storage = client.get_storage_client()
        content = storage.download_object(
            bucket_name=src_bucket, object_name=src_object
        )

        if os.path.isdir(dst):
            target_file = os.path.join(dst, src_filename)
        else:
            target_file = dst

        with open(target_file, "wb") as f:
            f.write(content)

    def _cp_file_to_object(self, opts, src, dst):
        if os.path.isdir(src):
            print("*** {} is a directory".format(src))
            return False

        dst_bucket, dst_object = _parse_ys_url(dst)
        if not dst_object:
            dst_object = os.path.basename(src)

        client = YamcsClient(**opts.client_kwargs)
        storage = client.get_storage_client()
        with open(src, "rb") as f:
            storage.upload_object(
                bucket_name=dst_bucket, object_name=dst_object, file_obj=f
            )
