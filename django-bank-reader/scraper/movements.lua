function main(splash)
  splash:init_cookies(splash.args.cookies)
  -- Loads MoneyMap page, this is done because next ajax request can't be made
  -- only on this page
  assert(splash:go{
    splash.args['moneymap_url'],
    headers=splash.args.headers,
    http_method=splash.args.http_method,
    })

  -- Builds ajax request to retrieve movements for specified month
  local js = string.format([[
    function main(splash) {
      $.post(
        "%s",
        {
          "meseanno": "%s",
          "dopoAggiornamento": "%s",
          "idBrand": "%s"
        }
      ).done(function(data) {
          splash.resume(data);
      })
      .fail(function() {
          splash.error();
      })
    }
    ]],
    splash.args.url,
    splash.args['meseanno'],
    splash.args['dopoAggiornamento'],
    splash.args['idBrand'])

  -- Executes ajax request previously created and gets its result
  local result, error = splash:wait_for_resume(js)
  assert(result)

  -- Waits a second
  splash:wait(1)

  -- Retrieves last response
  local entries = splash:history()
  local last_response = entries[#entries].response

  -- Returns ajax call url, Moneymap page request headers, status code, cookies
  -- and ajax call response
  return {
    url = splash.args.url,
    headers = last_response.headers,
    http_status = last_response.status,
    cookies = splash:get_cookies(),
    html = result['value'],
  }
end
