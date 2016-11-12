from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Post,Comment,Profile, Category, Tag
from django.contrib.admin.templatetags.admin_modify import prepopulated_fields_js

class ProfileInline(admin.StackedInline):
	model = Profile
	can_delete = False
	verbose_name_plural = 'profile'

class UserAdmin(BaseUserAdmin):
	inlines = (ProfileInline,)
	
	
admin.site.unregister(User)
admin.site.register(User,UserAdmin)
admin.site.register(Comment)

class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title', )}
    change_form_template = 'blog/admin/change_form.html'
    
    
admin.site.register(Post, PostAdmin)
admin.site.register(Profile)

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}
    
admin.site.register(Category, CategoryAdmin)

class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}

admin.site.register(Tag, TagAdmin)

