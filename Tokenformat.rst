===============
  Tokenformat
===============

.. contents::


----
 In
----

The Tokens are a 2 dimensional List.

It looks like This:
``[``

``[object, object, object],``

``[object, object]``

``]``

.. note:: That I also could write it like This:
          ``[[object, object, object],[object, object]]``


.. admonition:: For example

   ``[[Name("a"), Operant("="), Name("b"), Calc_Operant("-"), Integer(2)]]``

You can use ``object.type`` to view its type and ``object.data`` to look at the data.


-----
 Out
-----
Out comes a list of objects. These objects control the translator at the end.
The main job of the Tokenizer is it, to simplify the code:

.. admonition:: For example

                This: ``a=b*4-2`` to ``x=b*4`` ``y=x-2`` ``a=y``

Like I said before, these objects control the translator.
Here are the Objects:

+----------------------------+----------------------------+
|        Object              |        Use                 |
+============================+============================+
|``translator.add(a, b, x)`` |  Adds/divides/multiplies/  |
|``translator.mul(a, b, x)`` |  subtracts ore modules     |
|``translator.div(a, b, x)`` |  two numbers and stores    |
|``translator.sub(a, b, x)`` |  it in x.                  |
|``translator.mod(a, b, x)`` |                            |
+----------------------------+----------------------------+
|``translator.prt(str)``     |  Prints a string           |
|                            |                            |
|                            |                            |
|                            |                            |
|                            |                            |
|                            |                            |
|                            |                            |
|                            |                            |
|                            |                            |
|                            |                            |
+----------------------------+----------------------------+

The Tokenize function returns a list of tupels. These tupels contain at the first index the function.

.. warning:: Do **not** store these functions like this: ``(tranlator.mul(), [a, b, x])``.
             **Do** store them like this: ``(translator.add, [a, b, x])``
             You have to leave out the parantheses.

The second index is the list of arguments to this function.