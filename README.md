# SC2020-OctoTiger
Collection of configuration files and scripts to run the simulations on Cori

# Building, Running with APEX enabled
To build HPX with APEX enabled, just add the following to the CMake configuration:
```
-DHPX_WITH_APEX=TRUE \
```
to be explicit about what you want configured, add:
```
-DAPEX_WITH_ACTIVEHARMONY=FALSE \
-DAPEX_WITH_OTF2=FALSE \
-DAPEX_WITH_BFD=FALSE \
-DAPEX_WITH_PAPI=TRUE \
-DPAPI_ROOT=/path/to/papi/module/location \
-DHPX_WITH_APEX_NO_UPDATE=FALSE \
-DHPX_WITH_APEX_TAG=develop \
```
To get a screen output summary from rank/locality 0 at the end of execution, set the environment variable `APEX_SCREEN_OUTPUT=1`.  To get CSV profile output from all ranks/localities, set `APEX_CSV_OUTPUT=1`.  To see other APEX configuration settings, set `APEX_VERBOSE=1` before running.
