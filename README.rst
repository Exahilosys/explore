Installing
----------

.. code-block:: bash

  pip3 install explore

Quick Usage
-----------

.. code-block:: py

  import explore

  # yummy foods to choose from
  foods = ('pasta', 'glazed ham', 'salted broccoli', 'raw anchovy', 'peking duck')

  # choosing during a keyboard stroke
  food = explore.pick(foods, 'borlcoki')

More Complex
------------

.. code-block:: py

  import explore

  # lots of yummy food info
  foods = food_api.get_all()

  # match according to these attributes
  fetch = lambda food: (food.id, food.name, food.color)

  # generator of (food, score) pairs
  pairs = explore.generic(fetch, values, 'gween peepr')

  # best matching one
  food = explore.lead(pairs)


Links
-----

- `Documentation <https://explore.readthedocs.io>`_
