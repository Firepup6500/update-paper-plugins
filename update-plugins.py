from os import path, remove
from requests import request
from ast import literal_eval as litEval

# Try to load cache
print("[[  Info  ]] Trying to load installed versions from cache...")
knownVersions = {}
try:
    from cache import knownVersions

    print(f"[[  Info  ]] Loaded {len(knownVersions)} installed versions from cache...")
except ImportError:
    # Fallback to just a warning
    print(
        """||  Warn  || Failed to load versions from cache
||  Warn  || If this is not your first time running this script, it's recommended you investigate why."""
    )

hangarPlugins: dict[str, dict[str, str]] = {
    # "slug-of-plugin": {"Channel": "channel-to-pull", "Version": 'version-to-pull or "latest"'}
    "ViaBackwards": {"Channel": "Snapshot", "Version": "latest"},
}
spigotPlugins: dict[str, dict[str, str]] = {
    # "resource-id-of-plugin": {"Version": 'version-id-to-pull or "latest"', "Name": "Friendly name used for local downloads of the plugin"}
    "96927": {"Version": "latest", "Name": "DecentHolograms"},
}
# MOTE: I *want* to add modrinth here, but I can't figure out how to get the latest version of a project
# Also it'd be a pain to have *more* checks because modrinth also serves client-side mods
geyser = True
floodgate = True

if hangarPlugins:
    print("[[  Info  ]] Checking for updates in plugins from hangar")
    for plugin in hangarPlugins:
        print(f"[[  Info  ]] Checking for updates for plugin {plugin}")
        version = hangarPlugins[plugin]["Version"]
        if version == "latest":
            version = request(
                "GET",
                f"https://hangar.papermc.io/api/v1/projects/{plugin}/latest?channel={hangarPlugins[plugin]['Channel']}",
            ).text
            print(
                f"??  DBUG  ?? Latest version of {plugin} detected to be {version}, currently installed is {knownVersions[plugin] if knownVersions.get(plugin, False) else 'N/A'}"
            )
        if not knownVersions.get(plugin, "") or knownVersions[plugin] != version:
            # download update
            print(f"[[  Info  ]] Updating plugin {plugin}")
            with open(f"plugins/hangar-{plugin}-{version}.jar", "wb") as f:
                f.write(
                    request(
                        "GET",
                        f"https://hangar.papermc.io/api/v1/projects/{plugin}/versions/{version}/PAPER/download",
                    ).content
                )
            if knownVersions.get(plugin, "") and path.exists(
                f"plugins/hangar-{plugin}-{knownVersions.get(plugin, '')}.jar"
            ):
                remove(f"plugins/hangar-{plugin}-{knownVersions.get(plugin, '')}.jar")
            print(
                f"[[  Info  ]] Updated plugin {plugin} from {knownVersions[plugin] if knownVersions.get(plugin, False) else 'N/A'} to {version}"
            )
            knownVersions[plugin] = version
        else:
            print(f"[[  Info  ]] No updates available for {plugin}.")

if spigotPlugins:
    print("[[  Info  ]] Checking for updates in plugins from spigot")
    for plugin in spigotPlugins:
        pluginName = spigotPlugins[plugin]["Name"]
        print(f"[[  Info  ]] Checking for updates for plugin {pluginName}")
        version = spigotPlugins[plugin]["Version"]
        if version == "latest":
            version = litEval(
                request(
                    "GET",
                    f"https://api.spiget.org/v2/resources/{plugin}/versions/latest",
                ).text
            )["id"]
            print(
                f"??  DBUG  ?? Latest version of {pluginName}({plugin}) detected to be {version}, currently installed is {knownVersions[plugin] if knownVersions.get(plugin, False) else 'N/A'}"
            )
        if not knownVersions.get(plugin, "") or knownVersions[plugin] != version:
            with open(f"plugins/spigot-{pluginName}-{version}.jar", "wb") as f:
                f.write(
                    request(
                        "GET",
                        f"https://api.spiget.org/v2/resources/{plugin}/versions/{version}/download",
                    ).content
                )
            if knownVersions.get(plugin, "") and path.exists(
                f"plugins/spigot-{pluginName}-{knownVersions.get(plugin, '')}.jar"
            ):
                remove(
                    f"plugins/spigot-{pluginName}-{knownVersions.get(plugin, '')}.jar"
                )
            print(
                f"[[  Info  ]] Updated plugin {pluginName} from {knownVersions[plugin] if knownVersions.get(plugin, False) else 'N/A'} to {version}"
            )
            knownVersions[plugin] = version

if geyser:
    print(
        """[[  Info  ]] Updating geyser even if there isn't an update availiable
[[  Info  ]] Because my author is too lazy to implement proper update checking just for geyser and floodgate"""
    )
    with open("plugins/geyser.jar", "wb") as f:
        f.write(
            request(
                "GET",
                "https://download.geysermc.org/v2/projects/geyser/versions/latest/builds/latest/downloads/spigot",
            ).content
        )

if floodgate:
    print(
        """[[  Info  ]] Updating floodgate even if there isn't an update availiable
[[  Info  ]] Because my author is too lazy to implement proper update checking just for geyser and floodgate"""
    )
    with open("plugins/floodgate.jar", "wb") as f:
        f.write(
            request(
                "GET",
                "https://download.geysermc.org/v2/projects/floodgate/versions/latest/builds/latest/downloads/spigot",
            ).content
        )

# write cache file
with open("cache.py", "w") as f:
    f.write(f"knownVersions={knownVersions}")

print("[[  Info  ]] Updates complete!")
