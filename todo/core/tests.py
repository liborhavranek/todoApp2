from django.test import TestCase
from django.urls import reverse, resolve, reverse_lazy, path
from .views import (
    HomeView,
    TaskCreateView,
    User,
    Task,
    TaskUpdateView,
    TaskDetailView,
    TaskDeleteView,
    UserCreationForm,
    AdminUserList,
)

# Create your tests here.


class HomeViewTest(TestCase):
    def test_home_view_uses_correct_template(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home.html")

    def test_home_view_url_resolves_to_home_view(self):
        found = resolve("/")
        self.assertEqual(found.func.__name__, HomeView.as_view().__name__)


class TaskCreateViewTest(TestCase):
    def test_view_uses_correct_template(self):
        response = self.client.get(reverse_lazy("add_task"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "add_task.html")

    def test_create_view_url_resolves_to_create_view(self):
        found = resolve(reverse_lazy("add_task"))
        self.assertEqual(found.func.__name__, TaskCreateView.as_view().__name__)


class TaskUpdateViewTest(TestCase):
    def test_view_uses_correct_template(self):
        response = self.client.get(reverse_lazy("edit_task"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "edit_task.html")


class TaskUpdateViewTest(TestCase):
    # Setting up the test by creating a user and a task i need create user for create task and i add
    # task in the response like args with primary key
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.task = Task.objects.create(
            title="Test Title", text="Test Text", user=self.user
        )

    # Testing if the correct template is being used for the update view
    def test_update_view_uses_correct_template(self):
        # GET request if is used correct template for update view  self task.pk is primary key of task
        response = self.client.get(reverse("edit_task", args=[self.task.pk]))
        # assert if response code is 200
        self.assertEqual(response.status_code, 200)
        # assert if is correct template used
        self.assertTemplateUsed(response, "edit_task.html")

    def test_update_view_url_resolves_to_update_view(self):
        found = resolve("/edit_task/1")
        self.assertEqual(found.func.__name__, TaskUpdateView.as_view().__name__)


class TaskDetailViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.task = Task.objects.create(
            title="Test Title", text="Test Text", user=self.user
        )

    def test_detail_view_uses_correct_template(self):
        response = self.client.get(reverse("detail_task", args=[self.task.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "detail_task.html")

    def test_detail_view_url_resolves_to_detail_view(self):
        found = resolve("/detail_task/1")
        self.assertEqual(found.func.__name__, TaskDetailView.as_view().__name__)


class TaskDeleteViewTest(TestCase):
    def setUp(self):
        # create user and task
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.task = Task.objects.create(
            title="Test Title", text="Test Text", user=self.user
        )

    def test_delete_view_uses_correct_template(self):
        # login user and test template
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse("delete_task", args=[self.task.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "delete_task.html")

    def test_delete_view_url_resolves_to_delete_view(self):
        # test if is url is fit
        found = resolve("/delete_task/1")
        self.assertEqual(found.func.__name__, TaskDeleteView.as_view().__name__)

    def test_delete_view_deletes_correct_task(self):
        # test if correct task is deleted
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(reverse("delete_task", args=[self.task.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Task.objects.count(), 0)

    path("delete_task/<int:pk>/", TaskDeleteView.as_view(), name="delete_task"),


class CustomLoginViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )

    def test_login_view_uses_correct_template(self):
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "login.html")

    def test_login_view_redirects_authenticated_user(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse("login"))
        self.assertRedirects(response, reverse("task"))

    def test_login_view_redirects_to_task_on_success(self):
        response = self.client.post(
            reverse("login"), {"username": "testuser", "password": "testpassword"}
        )
        self.assertRedirects(response, reverse("task"))


class CustomRegisterViewTest(TestCase):
    # test if correct template is used
    def test_register_view_uses_correct_template(self):
        response = self.client.get(reverse("register"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "register.html")

    # test if is used correct form class
    def test_register_view__correct_form(self):
        response = self.client.get(reverse("register"))
        self.assertIsInstance(response.context["form"], UserCreationForm)


class AdminUserListTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )

    def test_url_registered(self):
        response = self.client.get(reverse("userlist"))
        self.assertEqual(response.status_code, 200)

    def test_get_queryset(self):
        response = self.client.get(reverse("userlist"))
        queryset = response.context["object_list"]
        self.assertEqual(queryset.model, User)
        self.assertIn("COUNT(", str(queryset.query))
        self.assertIn("task", str(queryset.query))
        self.assertIn("complete", str(queryset.query))
        self.assertIn("incomplete_task_count", str(queryset.query))
        self.assertIn("ORDER BY", str(queryset.query))


class AdminUserListURLTest(TestCase):
    # test what try find url userlist
    def test_user_list_url_resolves(self):
        url = reverse("userlist")
        self.assertEqual(resolve(url).func.view_class, AdminUserList)

    def test_user_list_url(self):
        response = self.client.get(reverse("userlist"))
        self.assertEqual(response.status_code, 200)


class UsersPageTest(TestCase):
    def test_users_page(self):
        response = self.client.get("/userlist")
        self.assertEqual(response.status_code, 200)
