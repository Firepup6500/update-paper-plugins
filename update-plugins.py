from dotenv import load_dotenv
from os import environ as env
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

load_dotenv()

hangarPlugins: dict[str, dict[str, str]] = {
    #    "slug-of-plugin": {"Channel": "channel-to-pull", "Version": 'version-to-pull or "latest"'}
}
spigotPlugins: dict[str, dict[str, str]] = {
    #    "resource-id-of-plugin": {"Version": 'version-id-to-pull or "latest"', "Name": "Friendly name used for local downloads of the plugin"}
}
geyser = True
floodgate = True
HANGAR_KEY = env.get("HANGAR_KEY", "")

if hangarPlugins and not HANGAR_KEY:
    print(
        """!! Notice !! This script cannot/will not download hangar plugins without a hangar api key!
!! Notice !! Please signup for an account at https://hangar.papermc.io/auth/signup
!! Notice !! Then generate an api key with the "view_public_info" permission at https://hangar.papermc.io/auth/settings/api-keys
!! Notice !! While I'm not 100% sure if they *enforce* the requirement, the API docs very clearly state that an API key is required.
!! Notice !! So even if it's not required *now* it could become enforced later.

!! Notice !! Since there's no hangar api key, the defined list of hangar plugins will be COMPLETELY IGNORED on this run."""
    )
    hangarPlugins = {}

if hangarPlugins:
    print("[[  Info  ]] Checking for updates in plugins from hangar")
    for plugin in hangarPlugins:
        print(f"[[  Info  ]] Checking for updates for plugin {plugin}")
        version = hangarPlugins[plugin]["Version"]
        if version == "latest":
            version = request(
                "GET",
                f"https://hangar.papermc.io/api/v1/projects/{plugin}/latest?channel={hangarPlugins[plugin]['Channel']}",
                headers = {"Authorization": f"Bearer ${HANGAR_KEY}"}
            ).text
            print(
                "??  DBUG  ?? Latest version of {plugin} detected to be {version}, currently installed is {knownVersions[plugin] if knownPlugins.get(plugin, False) else 'N/A'}"
            )
        if not knownVersions.get(plugin, "") or knownVersions[plugin] != version:
            # download update
            print(
                f"[[  Info  ]] Updating plugin {plugin}"
            )
            with open(f"plugins/hangar-{plugin}-{version}", "wb") as f:
                f.write(request("GET", f"https://https://hangar.papermc.io/api/v1/projects/{plugin}/versions/{version}/PAPER/download").content)
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
            # download update
            with open(f"plugins/spigot-{pluginName}-{version}", "wb") as f:
                f.write(request("GET", f"https://api.spiget.org/v2/resources/{plugin}/versions/{version}/download").content)
            print(
                f"[[  Info  ]] Updated plugin {pluginName} from {knownVersions[plugin] if knownVersions.get(plugin, False) else 'N/A'} to {version}"
            )
            knownVersions[plugin] = version

if geyser:
    # download https://download.geysermc.org/v2/projects/geyser/versions/latest/builds/latest/downloads/spigot
    ...

if floodgate:
    # download https://download.geysermc.org/v2/projects/floodgate/versions/latest/builds/latest/downloads/spigot
    ...

# write cache file
