from yamcs.client import YamcsClient

from yamcs.cli import utils


def AlgorithmCompleter(prefix, parsed_args, **kwargs):
    opts = utils.CommandOptions(parsed_args)
    client = YamcsClient(**opts.client_kwargs)
    mdb = client.get_mdb(opts.require_instance())
    return [x.qualified_name for x in mdb.list_algorithms()]


def BucketCompleter(prefix, parsed_args, **kwargs):
    opts = utils.CommandOptions(parsed_args)
    client = YamcsClient(**opts.client_kwargs)
    storage = client.get_storage_client()
    if not prefix:
        prefix = "ys://"

    if prefix in "ys://":
        return [f"ys://{b.name}/" for b in storage.list_buckets()]
    elif prefix.startswith("ys://"):
        _, path_prefix = utils.parse_ys_url(prefix)
        if path_prefix:
            return []
        return [f"ys://{b.name}/" for b in storage.list_buckets()]


def BucketOrObjectCompleter(prefix, parsed_args, **kwargs):
    opts = utils.CommandOptions(parsed_args)
    client = YamcsClient(**opts.client_kwargs)
    storage = client.get_storage_client()
    if not prefix:
        prefix = "ys://"

    if prefix in "ys://":
        return [f"ys://{b.name}/" for b in storage.list_buckets()]
    elif prefix.startswith("ys://"):
        bucket_name, path_prefix = utils.parse_ys_url(prefix)
        if path_prefix:
            listing = storage.list_objects(
                bucket_name, prefix=path_prefix, delimiter="/"
            )
            return [f"ys://{bucket_name}/{p}" for p in listing.prefixes] + [
                f"ys://{bucket_name}/{o.name}" for o in listing.objects
            ]
        elif prefix.endswith("/"):  # Bucket already entered, complete direct children
            listing = storage.list_objects(bucket_name, delimiter="/")
            return [f"ys://{bucket_name}/{p}" for p in listing.prefixes] + [
                f"ys://{bucket_name}/{o.name}" for o in listing.objects
            ]
        else:
            return [f"ys://{b.name}/" for b in storage.list_buckets()]


def CommandCompleter(prefix, parsed_args, **kwargs):
    opts = utils.CommandOptions(parsed_args)
    client = YamcsClient(**opts.client_kwargs)
    mdb = client.get_mdb(opts.require_instance())
    return [x.qualified_name for x in mdb.list_commands()]


def ContainerCompleter(prefix, parsed_args, **kwargs):
    opts = utils.CommandOptions(parsed_args)
    client = YamcsClient(**opts.client_kwargs)
    mdb = client.get_mdb(opts.require_instance())
    return [x.qualified_name for x in mdb.list_containers()]


def InstanceCompleter(prefix, parsed_args, **kwargs):
    opts = utils.CommandOptions(parsed_args)
    client = YamcsClient(**opts.client_kwargs)
    return [x.name for x in client.list_instances()]


def LinkCompleter(prefix, parsed_args, **kwargs):
    opts = utils.CommandOptions(parsed_args)
    client = YamcsClient(**opts.client_kwargs)
    return [x.name for x in client.list_links(opts.require_instance())]


def ParameterCompleter(prefix, parsed_args, **kwargs):
    opts = utils.CommandOptions(parsed_args)
    client = YamcsClient(**opts.client_kwargs)
    mdb = client.get_mdb(opts.require_instance())
    return [x.qualified_name for x in mdb.list_parameters()]


def ProcessorCompleter(prefix, parsed_args, **kwargs):
    opts = utils.CommandOptions(parsed_args)
    client = YamcsClient(**opts.client_kwargs)
    processors = client.list_processors(opts.require_instance())
    return [x.name for x in processors]


def ServiceCompleter(prefix, parsed_args, **kwargs):
    opts = utils.CommandOptions(parsed_args)
    client = YamcsClient(**opts.client_kwargs)
    return [x.name for x in client.list_services(opts.require_instance())]


def SpaceSystemCompleter(prefix, parsed_args, **kwargs):
    opts = utils.CommandOptions(parsed_args)
    client = YamcsClient(**opts.client_kwargs)
    mdb = client.get_mdb(opts.require_instance())
    return [x.qualified_name for x in mdb.list_space_systems()]


def StreamCompleter(prefix, parsed_args, **kwargs):
    opts = utils.CommandOptions(parsed_args)
    client = YamcsClient(**opts.client_kwargs)
    archive = client.get_archive(opts.require_instance())
    return [x.name for x in archive.list_streams()]


def TableCompleter(prefix, parsed_args, **kwargs):
    opts = utils.CommandOptions(parsed_args)
    client = YamcsClient(**opts.client_kwargs)
    archive = client.get_archive(opts.require_instance())
    return [x.name for x in archive.list_tables()]
