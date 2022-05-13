.. _event_watcher:

Event Watcher
######################################

Using the :ref:`Alias Python API (APA) <alias_python_api>`, the Engine can listen for events fired by Alias, and trigger Python callbacks. The :class:`alias_event_watcher.AliasEventWatcher` helps to manage registering callbacks for Alias Events, and ensuring that the callbacks are executed without interfering with Alias.

See the :ref:`APA Reference <alias_python_api-reference>` for the Alias Events that the Engine can register callbacks for.

.. currentmodule:: tk_alias.alias_event_watcher

.. autoclass:: AliasEventWatcher
    :show-inheritance:
    :members:
