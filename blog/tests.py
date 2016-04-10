from django.test import TestCase,RequestFactory
from . import views as page_view

from blog.models import Profile,Post
from django.contrib.auth.models import User,AnonymousUser

from django.utils import timezone

class TestInit(object):
	
	def setUpInit(self):
		self.factory=RequestFactory()
		self.plain_pw='test12345'
		self.user= User.objects.create_user(email='testinvestor@cgito.net',username='testinvestor',password=self.plain_pw,)
		
	def create_profile(self,user):
		profile=Profile(user=user,website='http://cgito.net')
		profile.save()
		return profile
		
	def create_post(self,profile):
	
		post=Post(poster=profile,title='Test post',text='Post description',pub_date=timezone.now())
		post.save()
		return post

class TestPage(TestCase,TestInit):
	post=None
	profile=None
	
	def setUp(self):
		self.setUpInit()
		
	
		
	
	
	def testPage(self):
		
		
		request = self.factory.get("/")
		
		home = page_view.index(request)
		self.assertEqual(home.status_code,200)
		
		request = self.factory.get("/login/")
		page=page_view.login_user(request)
		self.assertEqual(page.status_code,200)
		
		##print "page:",page
		
		
		
		
	#def testUser(self):
	def testPost(self):
		profile = self.create_profile(self.user)
		
		self.assertNotEqual(profile.website,"")
		self.assertGreater(profile.user.id,0)
		
		post=self.create_post(profile)
		
		##self.post=post
		self.assertGreater(post.id,0)
		##post.delete()
		
		request = self.factory.get("/login/")
		page=page_view.login_user(request)
		self.assertEqual(page.status_code,200)
		
		
		
		
		
		## should be login page
		
		request = self.factory.get("/blog/%d/" %(post.id,))
		request.user=AnonymousUser()
		#self.user
		page=page_view.comment(request)
		#print "content:%s" % (page.content,)
		self.assertEqual(page.status_code,200)
		
		comment_url="/blog/%d/comment/" %(post.id,)
		
		request = self.factory.get(comment_url)
		request.user=AnonymousUser()
		#self.user
		page=page_view.comment(request)
		#print "content:%s" % (page.content,)
		self.assertEqual(page.status_code,302)
		
		request = self.factory.get(comment_url)
		request.user=self.user
		page=page_view.comment(request)
		#print "content:%s" % (page.content,)
		self.assertEqual(page.status_code,200)
		
		
		
		request = self.factory.get("/logout/")
		page=page_view.logout_user(request)
		self.assertEqual(page.status_code,302)
		
		
		
	def testLogin(self):
	
		request = self.factory.get("/login/")
		page=page_view.login_user(request)
		self.assertEqual(page.status_code,200)

		request = self.factory.post("/login/",{'email':self.user.username, 'password':self.plain_pw})
		page=page_view.login_user(request)
		self.assertEqual(page.status_code,200)
	
		self.user.delete()
		
		
		