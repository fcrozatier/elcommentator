# Selenium

- The webdriver needs to be downloaded separalty, and placed in the PATH. It can be downloaded via homebrew or can be found on [selenium.org](https://www.selenium.dev/documentation/getting_started/installing_browser_drivers/)
- A good choice to place the webdriver is `\opt\webdriver\bin`
- The webdriver needs to correspond to your browser version

- To enable finer actions (drag, hold, right-click, tabs) you need `ActionChains`

  ```py
  from selenium.webdriver.common.action_chains import ActionChains
  actions = ActionChains(driver)
  ```

- To directly download pdf without opening them you need the following options:

  ```py
  from selenium.webdriver.chrome.options import Options
  from selenium.webdriver.common.keys import Keys

  expected_download = '~/Downloads/'
  opt = Options()
  opt.add_experimental_option("prefs", {
      'download.default_directory': expected_download,
      'download.prompt_for_download': False,
      'download.directory_upgrade': True,
      'plugins.always_open_pdf_externally': True
    })

  driver = Chrome(options=opt)
  ```
