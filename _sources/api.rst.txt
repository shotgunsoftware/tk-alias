.. _api:

API
####

Alias Python API
------------------

The Alias Python API is a Python module that provides a Pythoni interface to the Alias C++ API.

The Alias Toolkit Framework ``tk-framework-alias`` contains the Alias Python API module itself; the Alias Engine uses the framework to get the api module. Go to the `framework documentation <https://developers.shotgridsoftware.com/tk-framework-alias/alias_python_api.html>`_ to see the Alias Python API reference documentation.


AliasPy
--------

The Alias Python API can be accessed and used through the Alias Engine attribute ``alias_py``. This attribute is an :class:`AliasPy` intance, which is a wrapper around the Alias Python API module and provides addiional functionality to help interact with the Alias API. You can make Alias API calls using ``alias_py``; for example to call the API function create a shader:

.. code-block:: python

   # Create a shader using the Alias API
   shader = engine.alias_py.create_shader("MyShader")
   print(shader)

The additional :class:`AliasPy` modules are:

   * py_dag_node

   * py_layer

   * py_pick_list

   * py_utils

These modules provide added functionality to help make using the Alias API easier.

How to use the API effectively
--------------------------------

Since Alias 2024.0, the Alias Engine runs in its own separate process from Alias itself. The engine then uses Inter-process Communication (IPC) to interact with Alias. This adds a layer of communication when using the Alias API, which can slow down performance if the API is not used carefully:

**Key Understandings:**

* Each Alias API call made will incur the overhead of sending an IPC message

* Limit the number of API calls to improve performance

* Making an API call that returns a large data set will incur a larger overhead to send the data over IPC

Limiting the number of API calls will reduce the number of IPC messages sent between the Engine and Alias; this is really what affects the performance. So to limit the number of IPC messages, Alias API calls can be batched together and sent all in a single IPC message. This way you can still make the necessary API calls, while reducing the number of IPC messages sent. You can achieve this by using the ``AliasPy.request_context_manager`` method:

.. code-block:: python

   # Initialize a context manager to group the API calls into a single IPC message
   with engine.alias_py.request_context_manager():

      # First API call to clear the pick list
      self.alias_py.clear_pick_list()

      # Second API call to pick a list of given nodes
      self.alias_py.pick_nodes(nodes)

      # Third API call to redraw the screen
      self.alias_py.redraw_screen()

   # The context manager on exiting the above code scope will send all the API
   # calls in a single IPC message

You may execute the API calls asynchronously, which means the Alias Engine will not block and wait for the API operation to complete:

.. code-block:: python

   # Initialize a context manager to group the API calls into a single IPC message
   with engine.alias_py.request_context_manager(is_async=True):

      # First API call to clear the pick list
      self.alias_py.clear_pick_list()

      # Second API call to pick a list of given nodes
      self.alias_py.pick_nodes(nodes)

      # Third API call to redraw the screen
      self.alias_py.redraw_screen()

   # The context manager on exiting the above code scope will send all the API
   # calls in a single IPC message, and the Alias Engine will not wait for the result

If you need to get the result of the API calls made within the context manager, you can access the result from the manager object: 

.. code-block:: python

   # Wrap the API calls to create layers using the request context manager
    with engine.alias_py.request_context_manager() as manager:
      for i in range (100):
         layer_name = f"Layer{i}"
         engine.alias_py.create_layer(layer_name)

   # The context manager now on exiting the above code scope will send all
   # API calls in a single event, instead of 100 individual events

   # The result will be stored in the manager object `result` property, and it
   # will be a list of values returned from the API calls, in the order that the
   # API calls were made.
   for result in manager.result:
      print(result)

The Alias Engine does not support the ability to chain API calls together in a batch request; for example, the result of an API call is used to make a subsequent API call.

Avoid retrieving large data sets from the Alias API, if possible. Sending large data sets over IPC is expensive because the server must encode the data, include it in the message to the client, then the client must decode the data. For example, the API `search_` functions return :class:`TraverseDagOutputData` objects that contain the nodes found during the search operation, as well as the number of nodes found. If the search operations finds a large number nodes, then accessing them by :class:`TraverseDagOutputData.nodes` will be expensive, but accessing the number of nodes found by :class:`TraverseDagOutputData.count` will be very inexpensive. In this case, only access the nodes if absolutely necessary.

.. note::

   The Alias Object ``name`` property getter and :func:`type` do not require API calls, this data is stored on the client side. What this means is that you do not need to worry about access the Alias Object name or type.