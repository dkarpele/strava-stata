import swagger_client
from django.contrib.auth import get_user_model
from django.db.models import F, ExpressionWrapper, IntegerField
from django.db.models.functions import Round
from django.views.generic import ListView
from django.views.generic.base import TemplateView
from django_tables2 import SingleTableView
from swagger_client.rest import ApiException

from .models import Activities
from .tables import ActivitiesTable


class Home(TemplateView):
    template_name = 'stata/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.is_authenticated:
            title = f'Welcome to Strava Stata {user.first_name}!'
        else:
            title = f'Welcome to Strava Stata!'
        context["title"] = title
        return context


class ActivitiesUploadView(TemplateView):
    # paginate_by = 2
    template_name = 'stata/activities_upload.html'
    # context_object_name = 'activities_list'
    # model = get_user_model()
    allow_empty = True

    # Configure OAuth2 access token for authorization: strava_oauth
    configuration = swagger_client.Configuration()

    def get_queryset(self):
        activities = self.get_activities()
        current_db_ids = set(Activities.objects.values_list('activity_id',
                                                            flat=True))
        api_ids_set = {activity.id for activity in activities}
        api_ids_not_in_db = api_ids_set - current_db_ids
        if api_ids_not_in_db:
            for activity in activities:
                if activity.id in api_ids_not_in_db:
                    Activities.objects.create(
                        activity_id=activity.id,
                        name=activity.name,
                        distance=activity.distance,
                        elevation=activity.total_elevation_gain,
                        moving_time=activity.moving_time,
                        average_speed=activity.average_speed,
                        average_watts=activity.average_watts,
                        ride_type=activity.type,
                        date=activity.start_date_local,
                        location=activity.end_latlng)
        return Activities.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # context['activities'] = activities
        context['title'] = 'Activities'
        return context

    def get_access_token(self):
        user = get_user_model()
        self.configuration.access_token = user.objects.get().social_auth.get(
            provider='strava').access_token

    def get_activities(self):
        self.get_access_token()
        api_instance = swagger_client.ActivitiesApi(
            swagger_client.ApiClient(self.configuration))
        try:
            # List Athlete Activities
            api_response = api_instance.get_logged_in_athlete_activities(
                page=4)
            # print(swagger_client.AthletesApi(swagger_client.ApiClient(configuration))
            #       .get_stats(context.get('object_list').get().social_auth.get(provider='strava').uid))
            return api_response
        except ApiException as e:
            print(
                "Exception when calling ActivitiesApi->"
                "get_logged_in_athlete_activities: %s\n" % e)


class ActivitiesListView(SingleTableView):
    paginate_by = 15
    template_name = 'stata/activities_list_tables2.html'
    # context_object_name = 'activities_list'
    model = Activities
    allow_empty = True
    extra_context = {'title': 'Activities'}
    table_class = ActivitiesTable