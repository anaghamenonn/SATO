$(document).ready(function () {
    $('.payWithRazorPay').click(function (e) { 
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
            // alert("All fields are mandatory!!")
            swal("Alert!", "All fields are mandatory!", "error");
            return false;
        }
        else
        {
            $.ajax({
                method: "GET",
                url: "proceed-to-pay",
                success: function (response) {
                    console.log(response);
                    var options = {
                        "key": "rzp_test_NxknZ5LWLvnmLi",
                        "amount": 5000 , // Enter the Key ID generated from the Dashboard
                        // "amount": response.total_price , // Amount is in currency subunits. Default currency is INR. Hence, 50000 refers to 50000 paise
                        "currency": "USD",
                        "name": "SATO", //your business name
                        "description": "Thankyou for payment",
                        // "image": "https://example.com/your_logo",
                        // "order_id": "order_9A33XWu170gUtm", //This is a sample Order ID. Pass the `id` obtained in the response of Step 1
                        "handler": function (responseb){
                            console.log("Handler function triggered");
                            console.log("Razorpay Payment ID: " + responseb.razorpay_payment_id);
                            console.log("Form data: ", {
                                fname: fname,
                                lname: lname,
                                country: country,
                                address: address,
                                city: city,
                                state: state,
                                pincode: pincode,
                                phone: phone,
                                email: email,
                                payment_id: responseb.razorpay_payment_id
                            });
                            alert(responseb.razorpay_payment_id);
                            data = {
                                "fname" : fname ,
                                "lname" : lname,
                                "country" : country,
                                "address" : address,
                                "city" : city,
                                "state" : state,
                                "pincode" : pincode,
                                "phone" : phone,
                                "email" : email,
                                "payment_mode" : "Paid by Razorpay",
                                "payment_id" : responseb.razorpay_payment_id,
                                csrfmiddlewaretoken : token
                            }
                            console.log("Sending data to /placeorder endpoint");
                            $.ajax({
                                method: "POST",
                                url: "placeorder",
                                data: data,
                                success: function (responsec) {
                                    swal("Congratulations!", responsec.status, "success").then((value) => {
                                        window.location.href = '/orders'
                                    });
                                },
                                error: function (error) {
                                    console.error("Error placing order: ", error);
                                }
                            });
                            
                        },
                        "prefill": { //We recommend using the prefill parameter to auto-fill customer's contact information, especially their phone number
                            "name": fname+" "+lname, 
                            "email": email, 
                            "contact": phone  //Provide the customer's phone number for better conversion rates 
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