from django.conf.urls import patterns, url, include
from rest_framework_extensions.routers import ExtendedSimpleRouter
from .user import views as user_views
from .settings import views as settings_views
from .client import views as client_views
from .goals import views as goals_views
from .account import views as account_views
from .analysis import views as analysis_views
from .retiresmartz import views as retiresmartz_views
from .firm import views as firm_views
from .address import views as address_views
from .support import views as support_views
from .errorlog import views as errorlog_views
from .documents import views as documents_views
from .stripe_webhooks import stripe_webhook
from api.v1.user.views import PasswordResetView


router = ExtendedSimpleRouter(trailing_slash=False)
settings_router = router.register(r'settings',
                                  settings_views.SettingsViewSet,
                                  base_name='settings')
client_router = router.register(r'clients', client_views.ClientViewSet)
client_accounts_router = client_router.register(r'accounts',
                                                account_views.AccountViewSet,
                                                base_name='client-accounts',
                                                parents_query_lookups=['primary_owner'])
beneficiaries_router = client_router.register(r'beneficiaries',
                                              account_views.AccountBeneficiaryViewSet,
                                              base_name='account-beneficiaries',
                                              parents_query_lookups=['account__primary_owner'])

retirement_plans_router = client_router.register(r'retirement-plans',
                                                retiresmartz_views.RetiresmartzViewSet,
                                                base_name='client-retirement-plans',
                                                parents_query_lookups=['client'])
retirement_advice_router = retirement_plans_router.register(r'advice-feed',
                                                retiresmartz_views.RetiresmartzAdviceViewSet,
                                                base_name='client-retirement-advice',
                                                parents_query_lookups=['plan__client', 'plan'])

external_assets_router = client_router.register(r'external-assets',
                                                client_views.ExternalAssetViewSet,
                                                base_name='client-external-assets',
                                                parents_query_lookups=['owner'])

retirement_incomes_router = client_router.register(r'retirement-incomes',
                                                client_views.RetirementIncomeViewSet,
                                                base_name='client-retirement-incomes',
                                                parents_query_lookups=['plan__client'])
client_plaid_router = client_router.register(r'plaid',
                                             client_views.PlaidViewSet,
                                             base_name='plaid',
                                             parents_query_lookups=['client'])
client_quovo_router = client_router.register(r'quovo',
                                             client_views.QuovoViewSet,
                                             base_name='quovo',
                                             parents_query_lookups=['client'])
goals_router = router.register(r'goals',
                               goals_views.GoalViewSet)
goal_settings_router = goals_router.register(r'settings',
                                            goals_views.GoalSettingViewSet,
                                            base_name='goal-settings',
                                            parents_query_lookups=['goal'])
account_router = router.register(r'accounts',
                                 account_views.AccountViewSet)
account_goals_router = account_router.register(r'goals',
                                               goals_views.GoalViewSet,
                                               base_name='accounts-goal',
                                               parents_query_lookups=['account'])
documents_router = router.register(r'documents', documents_views.DocumentsViewSet)
plaid_router = router.register(r'plaid',
                               client_views.PlaidViewSet,
                               base_name='plaid')
quovo_router = router.register(r'quovo',
                               client_views.QuovoViewSet,
                               base_name='quovo')

urlpatterns = patterns(
    '',
    url(r'^me/?$', user_views.MeView.as_view(), name='user-me'),
    url(r'^me/profile/?$', client_views.ProfileView.as_view(), name='user-me-profile'),
    url(r'^me/profile/notifications/?$', client_views.EmailNotificationsView.as_view(), name='user-me-profile-notifications'),

    url(r'^user/(?P<pk>\d+)/?$', user_views.UserView.as_view(), name='user-user'),

    url(r'^register/?$', client_views.ClientUserRegisterView.as_view(), name='client-user-register'),
    url(r'^invites/(?P<invite_key>\w+)/?$', client_views.InvitesView.as_view(), name='invite-detail'),

    url(r'^user-names/?$', user_views.UserNamesView.as_view(), name='user-names'),

    url(r'^region/(?P<pk>\d+)/?$', address_views.RegionView.as_view(), name='region-detail'),

    url(r'^login/?$', user_views.LoginView.as_view(), name='user-login'),
    url(r'^returns$', analysis_views.ReturnsView.as_view()),

    url(r'^firm/', include('api.v1.firm.urls', namespace='firm')),
    url(r'^benchmarks/', include('api.v1.benchmarks.urls', namespace='benchmarks')),
    url(r'^validate/', include('api.v1.validation.urls', namespace='validate')),

    url(r'^me/password/?$', user_views.ChangePasswordView.as_view(), name='user-change-password'),
    url(r'^password/reset/?$', PasswordResetView.as_view(), name='password_reset'),

    url(r'me/firm/?$', user_views.UserFirmView.as_view(), name='user-firm'),
    url(r'me/security-questions/?$', user_views.SecurityQuestionAnswerView.as_view(), name='user-security-question'),
    url(r'me/security-questions/(?P<pk>\d+)/?$', user_views.SecurityQuestionAnswerUpdateView.as_view(), name='user-security-question-update'),
    url(r'me/security-questions/(?P<pk>\d+)/check/?$', user_views.SecurityAnswerCheckView.as_view(), name='user-check-answer'),

    # canned security messages, not user specific
    url(r'me/suggested-security-questions/?$', user_views.SecurityQuestionListView.as_view(), name='canned-security-questions'),

    url(r'^keep-alive/?$', user_views.KeepAliveView.as_view(), name='keep-alive'),

    url(r'^invites/(?P<invite_key>\w+)/resend/?$', client_views.ClientResendInviteView.as_view(), name='resend-invite'),

    url(r'^support-requests/?$', support_views.RequestAdvisorSupportView.as_view(), name='support-requests'),

    url(r'^stripe/?$', stripe_webhook, name='stripe-webhook'),

    url(r'^error/?$', errorlog_views.LogErrorView.as_view(), name='error-log'),
)

urlpatterns += router.urls
