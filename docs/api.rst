Alias Python API
####################################################

The Alias Engine is dependent on the Toolkit Framework ``tk-framework-alias`` to access the Alias Python API.

Since Alias 2024.0, the Alias Engine runs in its own separate process from Alias itself. The engine then uses Inter-process Communication (IPC) to interact with Alias. This adds a layer of communication when using the Alias API, which can slow down performance if the API is not used efficiently:

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

   # Initialize a context manager to group the API calls into a single IPC message
    with engine.alias_py.request_context_manager() as manager:
      for i in range (100):
         layer_name = f"Layer{i}"
         # This API call will be deferred until the context manager exits
         engine.alias_py.create_layer(layer_name)

   # The context manager on exiting the above code scope will send all the API
   # calls in a single IPC message
   # The result will be stored in the manager object `result` property, and it
   # will be a list of values returned from the API calls, in the order that the
   # API calls were made.
   for result in manager.result:
      print(result)

the Alias Engine does not support the ability to chain API calls together in a batch request; for example, the result of an API call is used to make a subsequent API call.

Avoid retrieving large data sets from the Alias API, if possible. Sending large data sets over IPC is expensive because the server must encode the data, include it in the message to the client, then the client must decode the data. For example, the API `search_` functions return :class:`TraverseDagOutputData` objects that contain the nodes found during the search operation, as well as the number of nodes found. If the search operations finds a large number nodes, then accessing them by :class:`TraverseDagOutputData.nodes` will be expensive, but accessing the number of nodes found by :class:`TraverseDagOutputData.count` will be very inexpensive. In this case, only access the nodes if absolutely necessary.