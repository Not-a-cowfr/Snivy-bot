from utils.playerUtils import get_online_status


def format_coins(value: float) -> str:
    if value < 0:
        return '-' + format_coins(-value)

    if value < 1000:
        return f'{value:.1f}'

    suffixes = ['k', 'm', 'b', 't']
    for i, suffix in enumerate(suffixes, 1):
        unit = 1000 ** i
        if value < unit * 1000:
            return f'{value / unit:.1f}{suffix}'
    return str(value)


def online_emoji(uuid):
    online_status = get_online_status(uuid)
    if online_status is False:
        return '🔴'
    elif online_status is True:
        return '🟢'
    else:
        return '❓'


# TODO change to custom rarity emojis
def rarity_emoji(rarity: str) -> str:
    rarity = rarity.lower()
    if rarity == 'common':
        return '<:common:1287356824970072064>'
    elif rarity == 'uncommon':
        return '<:uncommon:1287356840425816227>'
    elif rarity == 'rare':
        return '<:rare:1287356883660836985>'
    elif rarity == 'epic':
        return '<:epic:1287356897233600573>'
    elif rarity == 'legendary':
        return '<:legendary:1287356911620067420>'
    elif rarity == 'mythic':
        return '<:mythic:1287356929370357871>'
    elif rarity == 'divine':
        return '<:divine:1287356964615225415>'
    elif rarity == 'special':
        return '<:special:1287356982415851561>'
    else:
        return '❓'
