from booking.booking import Booking

try:
    with Booking(teardown=False) as bot:
        bot.land_first_page()
        bot.change_currency(currency='USD')
        bot.select_place_to_go('New York')
        bot.select_dates(check_in_date='2022-11-19',
                        check_out_date='2022-11-25')
        bot.select_adults(1)
        bot.click_search()
        bot.close_popup_apply_filtration()
        bot.all_pages_report_results()

except Exception as ex:
    if 'in PATH' in str(ex):
        print(
            'You are trying to run the bot from command line \n'
            'Please add to PATH your Selenium Drivers \n'
            'Windows: \n'
            '    set PATH=%PATH%;C:path-to-your-folder \n \n'
            'Linux: \n'
            '    PATH=$PATH:/path/toyour/folder/ \n'
        )
    else:
        raise