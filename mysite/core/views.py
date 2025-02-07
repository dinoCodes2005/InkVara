from django.shortcuts import render
from blogarea.models import Post

def home(request):
    # Get the first, second, and third highest posts based on likes
    top_posts = Post.objects.order_by('-like')[:3]

    # Assign posts if available
    first_highest_post = top_posts[0] if len(top_posts) > 0 else None
    second_highest_post = top_posts[1] if len(top_posts) > 1 else None
    third_highest_post = top_posts[2] if len(top_posts) > 2 else None

    context = {
        'first_highest_post': first_highest_post,
        'second_highest_post': second_highest_post,
        'third_highest_post': third_highest_post,
    }

    return render(request, 'home.html', context)
