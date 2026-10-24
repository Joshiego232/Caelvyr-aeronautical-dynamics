# Caelvyr Aeronautical Dynamics — Changelog

## Release V1.0.1
**Hangar, navigation, selector and forest improvements**

- Moved the aircraft-selection hangar to a separate preview area away from the active runway and gate spawn.
- Reworked aircraft, airport, start-position and settings panels with a more modern aviation-console interface and mobile-friendly layout.
- Added a selectable world airport map with tap/click airport markers, zoom controls and a fit-world action.
- Fixed the mobile MAP control to use the map's actual visibility state, and kept the flight map control available during flight.
- Added a RETURN TO TITLE SCREEN action to the pause menu.
- Added clustered forest population, with clusters targeting more than 100 successfully placed trees where terrain and biome rules allow.
- Added actual generated-tree and cluster counts by island, plus an ULTRA graphics preset for the densest supported forest pool.
- Increased instanced-tree capacity while avoiding per-tree shadow casting to reduce rendering cost.

**Forest-count note:** counts show actual positioned instances in the current bounded GPU instance pool. ULTRA raises the supported density, but this version does not claim millions of separately rendered tree objects per island; that scale needs a hierarchical forest/LOD system to remain practical on mobile.

## Release V1.0.0
**Initial Android release**

- Introduced the redesigned launch and title screens.
- Added the Play, Settings, and Plugins, Add-ons & Patches menus.
- Added aircraft selection and aircraft previews in the hangar.
- Added world and airport selection before starting a flight.
- Added graphics, flight assistance, and control configuration options.
- Introduced the in-app Check for Updates feature.
- Added release version information and changelog access.

### Planned improvements
- Expanded aircraft and airport selection.
- Additional graphics and performance settings.
- More controller configuration options.
- Further flight simulator refinements.
