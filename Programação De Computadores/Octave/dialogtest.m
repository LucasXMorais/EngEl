## create an empty dialog window titled "Dialog Example"
h = dialog ("name", "Dialog Example");

## create a button (default style)
b = uicontrol (h, "string", "OK",
                  "position", [10 10 150 40],
                  "callback", "delete (gcf)");

## wait for dialog to resume or close
uiwait (h);