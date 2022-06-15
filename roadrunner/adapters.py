from django import forms
from django.utils.translation import gettext as _

from django.utils.functional import cached_property
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string

from wagtail.admin.staticfiles import versioned_static
from wagtail.core.blocks.field_block import FieldBlockAdapter
from wagtail.core.blocks.stream_block import StreamBlockAdapter
from wagtail.core.blocks.struct_block import StructBlockAdapter
from wagtail.core.blocks.list_block import ListBlockAdapter


class RoadRunnerStreamBlockAdapter(StreamBlockAdapter):
    js_constructor = "roadrunner.fields.PreviewStreamBlockDefinition"

    def js_args(self, block):
        [name, grouped_child_blocks, values, meta] = super().js_args(block)
        meta["strings"]["APPLY"] = _("Apply")
        meta["strings"]["SAVING"] = _("Saving...")
        meta["strings"]["SAVE_DRAFT"] = _("Save Draft")
        return [name, grouped_child_blocks, values, meta]

    @property
    def media(self):
        return super().media + forms.Media(
            js=[
                versioned_static("wagtailadmin/js/telepath/blocks.js"),
                versioned_static("roadrunner/roadrunner.js"),
            ],
        )


class RoadRunnerStructBlockAdapter(StructBlockAdapter):
    js_constructor = "roadrunner.fields.StylingBlockDefinition"

    def js_args(self, block):
        name, values, meta = super().js_args(block)
        if hasattr(block.meta, "preview_template"):
            try:
                context = block.get_form_context(
                    block.get_default(), prefix="__PREFIX__", errors=None
                )
                meta["previewTemplate"] = mark_safe(
                    render_to_string(block.meta.preview_template, context)
                )
            except Exception as e:
                print(e)

        if hasattr(block.meta, "preview"):
            meta["preview"] = block.meta.preview

        return [name, values, meta]

    @cached_property
    def media(self):
        return super().media + forms.Media(
            js=[
                versioned_static("wagtailadmin/js/telepath/blocks.js"),
                versioned_static("roadrunner/roadrunner.js"),
            ],
        )


class RoadRunnerBaseBlockAdapter(RoadRunnerStructBlockAdapter):
    js_constructor = "roadrunner.fields.RoadRunnerBaseBlockDefinition"

    def js_args(self, block):
        name, values, meta = super().js_args(block)
        meta["classname"] = "struct-block roadrunnerblock"
        return [name, values, meta]

    @property
    def media(self):
        return super().media + forms.Media(
            css={"all": [versioned_static("roadrunner/roadrunner.css")]},
        )


class PreviewFieldBlockAdapter(FieldBlockAdapter):
    js_constructor = "roadrunner.fields.PreviewFieldBlockDefinition"

    @cached_property
    def media(self):
        return super().media + forms.Media(
            js=[
                versioned_static("wagtailadmin/js/telepath/blocks.js"),
                versioned_static("roadrunner/roadrunner.js"),
            ],
        )


class ImageChooserBlockAdapter(FieldBlockAdapter):
    js_constructor = "roadrunner.fields.ImageChooserBlockDefinition"

    @cached_property
    def media(self):
        return super().media + forms.Media(
            js=[
                versioned_static("wagtailadmin/js/telepath/blocks.js"),
                versioned_static("roadrunner/roadrunner.js"),
            ],
        )


class RichTextBlockAdapter(FieldBlockAdapter):
    js_constructor = "roadrunner.fields.RichTextBlockDefinition"

    @cached_property
    def media(self):
        return super().media + forms.Media(
            js=[
                versioned_static("wagtailadmin/js/telepath/blocks.js"),
                versioned_static("roadrunner/roadrunner.js"),
            ],
        )


class RoadrunnerRowBlockAdapter(ListBlockAdapter):
    js_constructor = "roadrunner.fields.RoadrunnerRowBlockDefinition"

    @cached_property
    def media(self):
        return super().media + forms.Media(  # pylint: disable=protected-access
            js=[
                versioned_static("wagtailadmin/js/telepath/blocks.js"),
                versioned_static("roadrunner/roadrunner.js"),
            ],
        )


class GridChoiceBlockAdapter(FieldBlockAdapter):
    js_constructor = "roadrunner.fields.GridChoiceBlockDefinition"


class ColorPickerBlockAdapter(FieldBlockAdapter):
    js_constructor = "roadrunner.fields.ColorPickerBlockDefinition"
