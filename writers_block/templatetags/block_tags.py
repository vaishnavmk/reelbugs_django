from django import template
from ..forms import Comment_form

register=template.Library()

@register.inclusion_tag('writers_block/blocks.html', takes_context=True)
def show_blocks(context):
	return{'block_list':context['block_list'], 'comment_form':context['comment_form'],'user':context['request'].user, 'request':context['request']}
