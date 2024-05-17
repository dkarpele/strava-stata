from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import ListView
import swagger_client
from swagger_client.rest import ApiException

# Configure OAuth2 access token for authorization: strava_oauth
configuration = swagger_client.Configuration()


class Home(ListView):
    template_name = 'stata/index.html'
    title_page = 'Home Page'
    extra_context = {'title': 'Home page'}
    context_object_name = 'qwerty'
    model = get_user_model()
    allow_empty = False


def get_access_token(context):
    user = context.get('object_list').get()
    social = user.social_auth.get(provider='strava')
    configuration.access_token = social.extra_data['access_token']


class Activities(ListView):
    template_name = 'stata/activities.html'
    title_page = 'Activities'
    extra_context = {'title': 'Activities'}
    context_object_name = 'activities'
    model = get_user_model()
    allow_empty = False

    # def get_queryset(self):
    #     return get_user_model()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        activities = self.get_activities(context)
        context['activities'] = activities
        return context

    def get_activities(self, context):
        get_access_token(context=context)
        api_instance = swagger_client.ActivitiesApi(
            swagger_client.ApiClient(configuration))
        try:
            # List Athlete Activities
            api_response = api_instance.get_logged_in_athlete_activities()
            print(swagger_client.AthletesApi(swagger_client.ApiClient(configuration))
                  .get_stats(context.get('object_list').get().social_auth.get(provider='strava').uid))
            return api_response
        except ApiException as e:
            print(
                "Exception when calling ActivitiesApi->"
                "get_logged_in_athlete_activities: %s\n" % e)
