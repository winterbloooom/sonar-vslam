from system import *
import scan_context_manager

slam_system = System("./parameters.yaml")
slam_system.load_params()
slam_system.create_scan_context_manager()
print("sc manager scs shape: ", len(slam_system.sc_manager.scan_contexts))

for idx, single_scan in enumerate(slam_system.scan_paths):
    print("current scan: ", single_scan)
    slam_system.sc_manager.add_node(single_scan, idx)
    # print("current scan context")
    # print(slam_system.sc_manager.scan_contexts[idx])
    scan_context_manager.visualize_scan_context(slam_system.sc_manager.scan_contexts[idx], idx)