
from django.contrib import admin
from django.urls import path
from customers import views as CustomerView
from wallet import views as walletView
from bankdetail import views as bankdetailView
from orders import views as OrderView
from content import views as contentView
from helpandsupport import views as helpandsupportView
from django.conf import settings
from django.conf.urls.static import static
from chats import views as chatView
from rate import views as rateView


urlpatterns = [
    path('admin/', admin.site.urls),
    # path("allcustomers/",CustomerView.customer),
    path("customersignin/",CustomerView.customer_signin),
    path("customersignup/",CustomerView.customer_signup),
    path("forgotpassword/",CustomerView.forgotpassword),
    path("verifyotp/",CustomerView.verify_otp),
    path("resetpassword/",CustomerView.reset_password),
    path("viewprofile/",CustomerView.view_profile),
    path("editprofile/",CustomerView.edit_profile),
    path("changepassword/",CustomerView.changepassword),
    path("orderrequest/",OrderView.order_request),
    path("allPendingForCustomer/",OrderView.pending_orders_for_customer),
    path("termsandcondition/",contentView.terms_and_condition),
    path("helpandsupport/",helpandsupportView.help_and_support),
    path("becomedriver/",CustomerView.become_driver),
    path("inprogressOrderForCustomer/",OrderView.progress_orders_for_customer),
    path("finishedOrderForCustomer/",OrderView.finished_orders_for_customer),
    path("countOrdersForCustomer/",OrderView.count_orders_for_customer),
    
    path("pendingOrderForDriver/",OrderView.pending_orders_for_drivers),
    
    
    
    path("inprogressOrderForDriver/",OrderView.progress_orders_for_driver),
    path("finishedOrderForDriver/",OrderView.finished_orders_for_driver),
    path("countOrdersForDriver/",OrderView.count_orders_for_driver),
    path("checkCustomerOrNot/",CustomerView.check_customer_or_not),
    path("editimage/",CustomerView.edit_image),
    path("allDriver/",CustomerView.all_driver),
    path("orderRequestChat/",chatView.order_request_chat),
    path("showChat/",chatView.show_chat),
    path("orderAcceptedAllDriverList/",OrderView.user_order_accepted),
    path("orderRequestChatFinal/",chatView.order_request_chat_final),
    
    path("admincommision/",contentView.admin_commision),
    path("accepteOrder/",OrderView.accepte_order),
    path("orderstatus/",OrderView.order_status),
    path("confirmprice/",chatView.confirm_price),
    
    path("completeOrder/",OrderView.complete_order),
    
    
    path("startchat/",chatView.start_chat),
    path("withdraw/",chatView.withdraw_order),
    path("decline/",chatView.decline_order),
    path("rate/",rateView.order_rate),
    path("wallethistory/",walletView.wallet_history),
    path("addBankDetail/",bankdetailView.add_bank_detail),
    path("showBankDetail/",bankdetailView.show_bank_detail)
    
    
]

if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)