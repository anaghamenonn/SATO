$(document).ready(function () {
    
    $('.paywithRazorpay').click(function (e) { 
        e.preventDefault();

        var fname = $("[name='fname']").val();
        var lname = $("[name='lname']").val();
        var country = $("[name='country']").val();
        var address = $("[name='address']").val();
        var city = $("[name='city']").val();
        var state = $("[name='state']").val();
        var pincode = $("[name='pincode']").val();
        var phone = $("[name='phone']").val();
        var email = $("[name='email']").val();
        var token = $("[name='csrfmiddlewaretoken']").val();

        if(fname == "" || lname == "" || country == "" || address == "" || city == "" || state == "" || pincode == "" || phone == "" || email == "")
        {
            swal("Alert!", "All fields are mandatory!", "error");
            return false;
        }
        else
        {
            $.ajax({
                method: "GET",
                url: "/proceed-to-pay",
                success: function (response) {
                    // console.log(response);
                    var options = {
                        "key": "rzp_test_XDXhWvjlFrJ7eB", 
                        "amount": response.total_price * 100,
                        "currency": "USD",
                        "name": "Vogue Stash",
                        "description": "Thank you for buying from us",
                        // "image": "C:\Users\anagh\Desktop\DapperStepp\Dapperstep\static\pr\img\mylogo.png",
                        // "order_id": "order_9A33XWu170gUtm", //This is a sample Order ID. Pass the `id` obtained in the response of Step 1
                        "handler": function (responseb){
                            alert(responseb.razorpay_payment_id);
                            data = {
                                "fname": fname,
                                "lname": lname,
                                "country": country,
                                "address": address,
                                "city": city,
                                "state": state,
                                "pincode": pincode,
                                "phone": phone,
                                "email" : email,
                                "payment_mode": "Paid by Razorpay",
                                "payment_id": responseb.razorpay_payment_id,
                                csrfmiddlewaretoken: token
                            }
                            $.ajax({
                                method: "POST",
                                url: "/placeorder",
                                data: data,
                                success: function (responsec) {
                                    swal("Congratulations!", responsec.status , "success").then((value) => {
                                      window.location.href = '/my-orders'
                                    });
                                }
                            });
                            
                        },
                        "prefill": { 
                            "name": fname+" "+lname,
                            "email": email,
                            "contact": phone
                        },
                        "theme": {
                            "color": "#3399cc"
                        }
                    };
                    var rzp1 = new Razorpay(options);
                    rzp1.open();
                }
            });

        }
        
        
       
    });
});



