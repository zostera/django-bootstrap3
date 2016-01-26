=======
Layouts
=======

The Rendering of Django Form can use a customized Layout to make it less linear.

By using the :class:`LayoutFormRenderer` as the default renderer, you can specify a customized layout in your form.

With Layout, you can take advantage of the bootstrap3 grid system to make your form more esthetic and more ergonomic.

---------------------------
1 - configure your settings
---------------------------

first, edit your settings.py to use the :class:`LayoutFormRenderer` :

.. code:: django


    BOOTSTRAP3 = {
        ...
        'form_renderers': {
            'default': 'bootstrap3.layout.LayoutFormRenderer',
        },
    }

--------------------
2 - give your layout
--------------------


then, configure your Layout in your form.py

^^^^^^^^^^^^^^^^^
Form.field_layout
^^^^^^^^^^^^^^^^^


you can give your layout either by giving it in :attr:`field_layout`:

.. code:: python


    class LayoutContactForm(forms.Form):
        name = forms.CharField()
        surname = forms.CharField()
        address = forms.CharField()
        address2 = forms.CharField()
        zipcode = forms.CharField()
        city = forms.CharField()
        country = forms.ChoiceField(choices=[("fr", "France"),("be", "belgium")])
        subject = forms.CharField()
        message = forms.CharField(widget=Textarea())

        fields_layout = [
            (
                [
                    ("name", "surname"),
                    "address",
                    "address2",
                    Row("zipcode", "city", zipcode=3, city=9),
                    "country"
                ],
                [
                    "subject",
                    "message",
                ]
            ),
        ]

^^^^^^^^^^^^^^^^^
Form.get_layout()
^^^^^^^^^^^^^^^^^


you can give your layout by overriding the  :meth:`get_layout` on the Form :

.. code:: python


    class LayoutContactForm(forms.Form):
        name = forms.CharField()
        surname = forms.CharField()
        address = forms.CharField()
        address2 = forms.CharField()
        zipcode = forms.CharField()
        city = forms.CharField()
        country = forms.ChoiceField(choices=[("fr", "France"),("be", "belgium")])
        subject = forms.CharField()
        message = forms.CharField(widget=Textarea())

        def get_layout(self)
            return [
                (
                    [
                        ("name", "surname"),
                        "address",
                        "address2",
                        Row("zipcode", "city", zipcode=3, city=9),
                        "country"
                    ],
                    [
                        "subject",
                        "message",
                    ]
                ),
            ]


----------------------
3 - create your layout
----------------------

The Layout hierarchy of :class:`LayoutElement` that will render
the fields for a given form. It is not dirrectly linked to the
form itself. So it can be reused for many form.

^^^^^^^^^
the rules
^^^^^^^^^

1. a field *in* the layout and  *in* the final form will be *rendered* (of cours)
2. a field *in* the layout but *not in* the final form will **silently** be *skiped*
3. a field *not in* the layout but *in* the final form will **silently** be *rendered* (see :class:`EllipsisFieldContainer`)

This mean that a Layout must not match exactly the form. It will do the job silently.

.. note ::

  all missings field in the layout (rule 3) will be rendered by the :class:`EllipsisFieldContainer` of the layout. this
  LayoutElement must be uniq (and will check for it). If you dont manualy provide one in your layout, the Layout class
  will add one at his own end. so basicaly, all missing field will be rendered at the end of the form.

^^^^^^^^^^^^^^^^^^^^^^^^^
the structure of a Layout
^^^^^^^^^^^^^^^^^^^^^^^^^

to create a layout, you can give a nested suit of tuple/list and some unicode to add a field.
it will try to create a valid suit of row/col in the final rendering.

at the rendering time, your nested structur will be transformed into a native :class:`LayoutElement` structure and
finally rendered.

""""""
simple
""""""

the following layout :

.. code::

    fields_layout = [
        "subject",
        "message",
    ]

will be equivalent to  :

.. code::

    fields_layout = Layout(
        FieldContainer("subject"),
        FieldContainer("message")
    )


and be rendered in something like ::

   [subject                     ]

   [message                     ]
   [                            ]
   [                            ]


""""""
nested
""""""

and the more complexe layout :

.. code::

    fields_layout = [
        ("name", "surname"),
        "message",
    ]

will be equivalent to  :

.. code::

    fields_layout = Layout(
        Row(Col(FieldContainer("name")), Col(FieldContainer("surname"))),
        FieldContainer("message")
    )

and be rendered in something like ::

   [name        ] [surname      ]

   [message                     ]
   [                            ]
   [                            ]


"""""
mixed
"""""


You can insert any :class:`LayoutElement` in this suit, at any place. this will prevent the automatic guessing of
the desired :class:`LayoutElement` and force your element in the chain.


.. code::

    fields_layout = [
        Row(Col(FieldContainer("name")), Col(FieldContainer("surname"))),
        "message",
    ]

will be equivalent to  :

.. code::

    fields_layout = Layout(
        Row(Col(FieldContainer("name")), Col(FieldContainer("surname"))),
        FieldContainer("message")
    )

and be rendered in something like ::

   [name        ] [surname      ]

   [message                     ]
   [                            ]
   [                            ]

the first row is as you wished it, and the message will be guessed.

.. warning::

  but take care to insert your element in the good place :

  .. code::

      fields_layout = [
          ("name", "surname"),
          Row(FieldContainer("message")),
      ]

  will be equivalent to

  .. code::

      fields_layout = Layout(
          Row(Col(FieldContainer("name")), Col(FieldContainer("surname"))),
          Row(FieldContainer("message")),
      )

  and be rendered in something like ::

     [name        ] [surname      ]

    [message                       ]
    [                              ]
    [                              ]

  it is subtle, but the "message" is directly in the Row, and no column is present to match
  the negative margin of the row. so your message will be larger than the grid intended to.

  adding a Col without a parent row will give the same problem. the usage of list/tuple/str take
  care of thes problem and shall creat the Col and Row properly.


-------------------------
4 - customize your layout
-------------------------

Many LayoutElement can be cusomized if inserted manualy in their native form (By Instacing the class).
since the layout can be `mixed`, you can take the best of the guessing feature and insert your native class into it.

^^^
Col
^^^

.. py:class:: Col(*childs, size=None)

  :param childs: all child contained in this column
  :param size: the size the column will take on the grid (bootstrap have a 12 column grid)


the :class:`Col` will create a `<div class="col-xx-yy">...</div>` in your layout. it should always be included in a
:class:`Row`. his size on the grid can be given by the `size` attribute. each other elements will be added in the Col.

if the size is not given or is None, the parent Row will fix it to give equal size for all his children.

.. code::

  Row(Col("name"), Col("surname")) # both fields will have a size of 6 (class="col-md-6")
  Row(Col("name", size=4), Col("surname", size=8)) # name will have a size of 4 and surname a size of 8 column



^^^
Row
^^^
.. py:class:: Row


the :class:`Row` will create as many column as it have childs, each one of the same size if possible::

  # will give each column a size of 6
  Row("name", "surname")

  # will alocate a size of 10 to name since `surname` take only 2
  Row("name", Col("surname", size=2))


.. warning::

  a :class:`Row` should contains Col as childs

  good::

    Row(Col("name"), Col("surname"))

  bad::

    # row can't contains Row
    Row(Row(Col("name"), Col("surname")))
    # Row should contains Column and nothing else
    Row(FieldContainer("name"))

  Remember that if you give a unicode/list/tuple to the row, it will take care of creating each column for you. fell free to do ::

    Row("name", "surname")

^^^^^^^^^^^^^^
FieldContainer
^^^^^^^^^^^^^^

.. py:class:: FieldContainer

  :param fieldname: the name of the field

the :class:`FieldContainer` is just the final part of the layout. it will basicaly render the field itself and nothing more.

in fact, all str given in the layout will be used as a FieldContainer


^^^^^^
Layout
^^^^^^

.. py:class:: Layout


The :class:`Layout` is the root element of a Layout. it is automaticaly created using the whole layout you give in fields_layout::

  # following is equivalent
  fields_layout = ["name", "surname"]
  fields_layout = Layout("name", "surname")

it will create the final :class:`EllipsisFieldContainer` if none is present in the given layout

^^^^^^^^^^^^^^^^^^^^^^
EllipsisFieldContainer
^^^^^^^^^^^^^^^^^^^^^^

.. py:class:: EllipsisFieldContainer

This element is in charge of adding all missing fields of the form into the final rendering.
if a field is not present in the Layout, but is in the form, this field will render all of them in the
order they are declared in the form.

you can provide a EllipsisFieldContainer in a part of your layout like that ::

    fields_layout = [ # Layout
        ( # Row
            [ # col-md-6
                "name",
                "surname",

            ],
            [ # col-md-6
                # will render all fields of the form other than "name" and "surname" in a
                # column right to these two.
                EllipsisFieldContainer()
            ]
        ),
    ]

you can give the `Ellipsis` global value to create a EllipsisFieldContainer. it is equivalent ::

    fields_layout = [ # Layout
        ( # Row
            [ # col-md-6
                "name",
                "surname",

            ],
            [ # col-md-6
                ... # python 3 only
                # or
                Ellipsis # python 2 and 3
            ]
        ),
    ]


.. note::

  Only one :class:`EllipsisFieldContainer` can be added to a Layout. it will raise a :class:`BootstrapException` if a 2nd EllipsisFieldContainer is
  inserted in the layout.

.. note::

  the Layout will add a :class:`EllipsisFieldContainer` automaticaly if none is present in the given layout