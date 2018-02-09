#! /bin/bash

/home/irg/tungsten/tungsten/tools/tpm update --hosts=boat,shore --repl-svc-applier-filters=delay,replicate --property=replicator.filter.delay.delay=60 --property=replicator.filter.replicate.ignore=xgds_basalt.xgds_video_videosegment,xgds_basalt.xgds_video_videoepisode,xgds_basalt.xgds_core_constant,xgds_basalt.xgds_status_board_subsystem,xgds_basalt.xgds_status_board_subsystemgroup,xgds_basalt.xgds_core_relayevent,xgds_basalt.xgds_core_relayfile,xgds_basalt.basaltApp_basaltactiveflight

ssh boat ./tungsten/tungsten/tools/tpm update --hosts=boat,shore --repl-svc-applier-filters=delay,replicate --property=replicator.filter.delay.delay=60 --property=replicator.filter.replicate.ignore=xgds_basalt.xgds_video_videosegment,xgds_basalt.xgds_video_videoepisode,xgds_basalt.xgds_core_constant,xgds_basalt.xgds_status_board_subsystem,xgds_basalt.xgds_status_board_subsystemgroup,xgds_basalt.xgds_core_relayevent,xgds_basalt.xgds_core_relayfile,xgds_basalt.basaltApp_basaltactiveflight
