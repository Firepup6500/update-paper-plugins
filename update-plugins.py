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
    print("""[[  Warn  ]] Failed to load versions from cache
[[  Warn  ]] If this is not your first time running this script, it's recommended you investigate why.""")

load_dotenv()

hangarPlugins = {
    #    "slug-of-plugin": {"Channel": "channel-to-pull", "Version": 'version-to-pull or "latest"'}
}
spigotPlugins = {
    #    "resource-id-of-plugin": {"Version": 'version-id-to-pull or "latest"', "Name": "Friendly name used for local downloads of the plugin"}
}
geyser = True
floodgate = True

if hangarPlugins and not env.get("HANGAR_KEY", ""):
    print(
        """!! Notice !! This script cannot download hangar plugins without a hangar api key!
!! Notice !! Please signup for an account at https://hangar.papermc.io/auth/signup
!! Notice !! Then generate an api key with the "view_public_info" permission at https://hangar.papermc.io/auth/settings/api-keys

!! Notice !! Since there's no hangar api key, the defined list of hangar plugins will be COMPLETELY IGNORED on this run."""
    )
    hangarPlugins = {}

if hangarPlugins:
    for plugin in hangarPlugins:
        version = hangarPlugins[plugin]["Version"]
        if version == "latest":
            version = request("GET", f"https://hangar.papermc.io/api/v1/projects/{plugin}/latest?channel={channel}").text
        if not knownVersions.get(plugin, "") or knownVersions[plugin] != version:
            # download update
            knownVersions[plugin] = version

if spigotPlugins:
    for plugin in spigotPlugins:
        version = spigotPlugins[plugin]["Version"]
        if version == "latest":
            version = litEval(request("GET", f"https://api.spiget.org/v2/resources/{plugin}/versions/latest").text)["id"]
        if not knownVersions.get(plugin, "") or knownVersions[plugin] != version:
            # download update
            knownVersions[plugin] = version

if geyser:
    # download https://download.geysermc.org/v2/projects/geyser/versions/latest/builds/latest/downloads/spigot
    ...

if floodgate:
    # download https://download.geysermc.org/v2/projects/floodgate/versions/latest/builds/latest/downloads/spigot
    ...

# write cache file
