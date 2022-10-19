.. _hooks:

Alias Engine Hooks
======================

The Alias Engine defines hooks to customize the Toolkit Apps that it uses. See below for App specific hook details.

.. _hooks-tk-multi-data-validation:

tk-multi-data-validation
--------------------------

.. _hooks-tk-multi-data-validation-data-validator:

AliasDataValidationHook
^^^^^^^^^^^^^^^^^^^^^^^^^

This hook will get the validation rule data from the :ref:`data_validator` and pass it to the tk-multi-data-validation App.

.. literalinclude:: ../hooks/tk-multi-data-validation/basic/data_validation.py
    :language: python

.. _hooks-tk-multi-loader2:

tk-multi-loader2
--------------------------

.. _hooks-tk-multi-loader2-scene-actions:

AliasActions
^^^^^^^^^^^^^^^^^^^^^^^^^

.. literalinclude:: ../hooks/tk-multi-loader2/basic/scene_actions.py
    :language: python

.. _hooks-tk-multi-publish2:

tk-multi-publish2
--------------------------

.. _hooks-tk-multi-publish2-publish-annotations:

PublishAnnotationsPlugin
^^^^^^^^^^^^^^^^^^^^^^^^^

.. literalinclude:: ../hooks/tk-multi-publish2/basic/publish_annotations.py
    :language: python

.. _hooks-tk-multi-publish2-publish-session:

AliasSessionPublishPlugin
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. literalinclude:: ../hooks/tk-multi-publish2/basic/publish_session.py
    :language: python

.. _hooks-tk-multi-publish2-publish-translation:

AliasTranslationPublishPlugin
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. literalinclude:: ../hooks/tk-multi-publish2/basic/publish_translation.py
    :language: python

.. _hooks-tk-multi-publish2-publish-variants:

AliasPublishVariantsPlugin
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. literalinclude:: ../hooks/tk-multi-publish2/basic/publish_variants.py
    :language: python

.. _hooks-tk-multi-publish2-start-version-control:

AliasStartVersionControlPlugin
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. literalinclude:: ../hooks/tk-multi-publish2/basic/start_version_control.py
    :language: python

.. _hooks-tk-multi-publish2-upload-version:

UploadVersionPlugin
^^^^^^^^^^^^^^^^^^^^^^^^^

.. literalinclude:: ../hooks/tk-multi-publish2/basic/upload_version.py
    :language: python

tk-multi-shotgunpanel
--------------------------

.. _hooks-tk-multi-shotgunpanel-scene-actions:

AliasActions
^^^^^^^^^^^^^^^^^^^^^^^^^

.. literalinclude:: ../hooks/tk-multi-shotgunpanel/basic/scene_actions.py
    :language: python

tk-multi-workfiles2
--------------------------

.. _hooks-tk-multi-workfiles2-scene-operations:

SceneOperation
^^^^^^^^^^^^^^^^^^^^^^^^^

.. literalinclude:: ../hooks/tk-multi-workfiles2/basic/scene_operation.py
    :language: python
