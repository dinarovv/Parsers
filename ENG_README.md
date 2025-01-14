Avito Parser info:
------------------------------
**********
  How to use it:
  
  Calling the parse() function from:
  1) your city in English. (Examples: 'moscow','chelyabinsk',...) (P.S. It doesn't work from someone else's city!!!)
  2) the name is one of the sections of Avito. (Examples: 'tovary_dlya_kompyutera','bytovaya_elektronika',...)
**********
  Additional information:

  • A user agent is used (everything can work without it too). It is needed to visit the site freely as a user, not as a bot.
  
  • The parser converts the page content into an object (soup) that can be used to search for HTML elements.
  
  • HTML classes are transferred to the code by analyzing the code of the page element (f12).

  • Each ad is placed in the list of products with a dictionary of the form: {key - name of the item/service: item - price}.
