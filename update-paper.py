from requests import request
import firepup650 as fp

fp.replitCursor = f"{fp.bcolors.REPLIT}> {fp.bcolors.RESET}"
version = fp.replitInput("What minecraft version would you like?").strip('" ')
experimental = (
    fp.replitInput("Should I try to get an experimental build? (y|N)")
    .lower()
    .strip()
    .startswith("y")
)

print("[[  Info  ]] Requesting availiable paper versions")
versions = request("GET", "https://api.papermc.io/v2/projects/paper").json()["versions"]
if version not in versions:
    exit(
        f"!! ERROR  !! Version {version} is not availiable. Please select from {versions}"
    )

builds = []
print(f"[[  Info  ]] Requesting availiable builds for {version}")
builds = request(
    "GET", f"https://api.papermc.io/v2/projects/paper/versions/{version}/builds"
).json()["builds"]

if not experimental:
    print("[[  Info  ]] Selecting only 'default' builds")
    i = 0
    for build in builds:
        if build["channel"] != "default":
            del builds[i]
        i += 1
    del i

if not builds:
    exit(
        f"!! ERROR  !! No builds availiable for version {version}, perhaps only experimental ones are availiable?"
    )

build = builds[-1]["build"]

print(
    f"""[[  Info  ]] Selected build {build}
[[  Info  ]] Downloading selected build"""
)

with open(f"paper-{version}.jar", "wb") as f:
    f.write(
        request(
            "GET",
            f"https://api.papermc.io/v2/projects/paper/versions/{version}/builds/{build}/downloads/paper-{version}-{build}.jar",
        ).content
    )

print(
    f"""[[  Info  ]] Downloaded selected build as paper-{version}.jar
[[  Info  ]] If you're upgrading MC versions, please retain your old server jar
[[  Info  ]] And backup your world folders before running the new paper version

[[  Info  ]] All done!"""
)
