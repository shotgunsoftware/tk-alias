What's Changed
####################################################

v4.0.0
-------

* New method :func:`AliasPy.request_context_manager`

* New method :func:`AliasPyDagNode.is_template`

* New method :func:`AliasPyDagNode.is_instance`

* New method :func:`AliasPyDagNode.has_zero_transform`

* New method :func:`AliasPyDagNode.has_origin_pivot`

* Removed class :class:`AliasPyTraverseDag`. Applicable class functions have been moved to :class:`AliasPyDagNode`

   * Attribute will no longer be available from the engine: :class:`AliasEngine.alias_py.py_traverse_dag`

* Removed parameter ``check_exists`` from the following functions:

      * :func:`AliasPyDagNode.get_instanced_node`

      * :func:`AliasPyDagNode.get_nodes_with_construction_history`

      * :func:`AliasPyDagNode.get_nodes_with_non_zero_transform`

      * :func:`AliasPyDagNode.get_nodes_with_non_origin_pivot`

      * :func:`AliasPyDagNode.get_nodes_with_unused_curves_on_surface`

   * This affects :class:`AliasEngine.alias_py.py_dag_node`

* Removed parameter ``check_exists`` from function :func:`AliasPyLayer.get_symmetric_layers`

      * This affects :class:`AliasEngine.alias_py.py_layer`

* Removed parameter ``skip_shaders`` from function :class:`AliasPyPickList.pick_nodes_assigned_to_shaders`

   * This affects :class:`AliasEngine.alias_py.py_pick_list`
