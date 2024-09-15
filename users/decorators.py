from django.http import HttpResponse
from django.shortcuts import redirect, render

def role_required(role):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if not hasattr(request.user, f'is_{role}') or not getattr(request.user, f'is_{role}', False):
                redirect_urls = {
                    'journalist': '/users/journalist_dashboard/',
                    'editor': '/editor_dashboard/',
                    'head': '/head_dashboard/'
                }

                for user_role, redirect_url in redirect_urls.items():
                    if getattr(request.user, f'is_{user_role}', False):
                        # Render the error page template with a redirect URL
                        return render(request, 'users/error_redirect.html', {
                            'redirect_url': redirect_url
                        })

                # If no valid role is found, redirect to login page
                return redirect('')
            
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator


def login_required_redirect(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('users:login')  # Redirect to login if not authenticated
        return view_func(request, *args, **kwargs)
    return _wrapped_view