from authentication.models import User
from nft.models import NftImage, NftPost, Collection
from django.template.loader import render_to_string


def user_nft_html(user: User):
    images = NftImage.objects.filter(owner=user)
    return render_to_string(
        template_name='nft/my-nft.html',
        context={'images': images, 'user': user}
    )


def collections_html(user: User):
    collections_list = Collection.objects.all()
    return render_to_string(
        template_name='nft/collections.html',
        context={'collections': collections_list, 'user': user}
    )


def marketplace_html(user: User):
    posts = NftPost.objects.all()
    return render_to_string(
        template_name='nft/marketplace.html',
        context={'posts': posts, 'user': user}
    )


def get_collections_list(user):
    collections_list = Collection.objects.filter(changeable=True)
    result = []
    for collection in collections_list:
        flag = True
        collection_images = collection.images.all()
        for image in collection_images:
            if image.owner != user:
                flag = False
        if flag:
            result.append({'name': collection.name, 'id': collection.id})
    return result


def get_nft_info_html(user: User, nft_id: int):
    image = NftImage.objects.get(pk=nft_id)
    posts = NftPost.objects.filter(image=image)
    can_sell = False if len(posts) else True
    html = render_to_string(template_name='nft/nft-info.html',
                            context={'image': image, 'can_sell': can_sell})
    if can_sell:
        html += render_to_string(template_name='nft/modal/sell_nft.html',
                                 context={'image': image, 'can_sell': can_sell})
    return html


def select_nft_section(user: User, nft_id: int):
    image = NftImage.objects.get(pk=nft_id)
    return 'my-nft' if image.owner == user else 'collections'


def select_post_section(user: User, post_id: int):
    post = NftPost.objects.get(pk=post_id)
    return 'my-nft' if post.image.owner == user else 'marketplace'


def get_post_html(user: User, post_id: int):
    post = NftPost.objects.get(pk=post_id)
    balance = getattr(user, post.currency)
    return render_to_string(
        template_name='nft/nft-info.html',
        context={'image': post.image, 'can_sell': False}
    ) if post.image.owner == user else render_to_string(
        template_name='nft/post_info.html',
        context={'post': post, 'balance': balance}
    )


def create_nft(user: User, data: dict, file):
    if data['collection'] == 'Create-new-collection':
        collection = Collection(name=data['new_collection'])
        collection.save()
    else:
        collection = Collection.objects.get(pk=data['collection'])
    new_img = NftImage(
        img=file,
        name=data['name'],
        price=data['price'],
        currency=data['currency'],
        collection=collection,
        owner=user
    )
    new_img.save()


def sell_nft(data: dict):
    image = NftImage.objects.get(pk=data['id'])
    image.collection.changeable = False
    image.collection.save()
    new_post = NftPost(image=image, price=data['price'], currency=data['currency'])
    new_post.save()


def buy_nft(user: User, data: dict):
    post = NftPost.objects.get(pk=data['id'])
    balance = getattr(user, post.currency)
    setattr(user, post.currency, balance - post.price)
    balance = getattr(post.image.owner, post.currency)
    setattr(post.image.owner, post.currency, balance + post.price)
    post.image.currency = post.currency
    post.image.price = post.price
    post.image.owner = user
    post.image.save()
    post.image.owner.save()
    user.save()
    post.delete()
