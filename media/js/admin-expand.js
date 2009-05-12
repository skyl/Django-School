/* Selectively expands and collapses installed Django apps in the main Django
 * Admin page. If jquery.cookie.js [1] is available, it will remember which apps you
 * have expanded.
 *
 * .. [1] http://dev.jquery.com/browser/trunk/plugins/cookie/jquery.cookie.js
 */

$(document).ready(function() {
    var cookie_name = "admin_expanded";
    var delim = "|";
    var admin_expanded = [];
    var base_selector = $("body.dashboard #content-main .module caption");

    // if the cookie plugin is available
    if ($.isFunction($.cookie)) {
        // put any expanded modules in the expanded list
        $.each(($.cookie(cookie_name) || "").split(delim), function(index, obj) {
            if (obj) { admin_expanded.push(base_selector.filter("caption:contains('"+obj+"')")[0]); }
        });
    }

    // minor usability fix
    base_selector.css("width", "100%").css("cursor", "pointer");

    // collapse all modules that aren't remembered in the cookie
    base_selector.not(admin_expanded).siblings('tbody').hide();

    // toggle on click
    base_selector.click(function(){
        $(this).siblings('tbody').animate({opacity: 'toggle'}, "fast", null, function(){
            // if the cookie plugin is available
            if ($.isFunction($.cookie)) {
                // set or remove this module in the cookie
                t = $(this).siblings('caption').text();
                j = ($.cookie(cookie_name) || "").split(delim);
                if (j.indexOf(t) != -1) {
                    j.splice(j.indexOf(t), 1);
                } else {
                    j.push(t);
                }
                $.cookie(cookie_name, j.join("|"));
            }
        });
    });
});

