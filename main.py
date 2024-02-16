items = ["one", "two", "three", "four"]

lines = {"windows": {}, "max": 0}


def addlin(lines, window, content):
  if window not in lines["windows"]:
    lines["windows"][window] = []
  lines["windows"][window].append(content)
  lines["max"] = max(lines["max"], len(lines["windows"][window]))


for item in items:
  addlin(lines, 0, "[+] {}".format(item))
  addlin(lines, 1, "[+] {}".format(item))

width = 50
height = 600
grid = [["vert", [["hoz", [["windows", [["window", 0], ["window", 1]]]]]]]]

data = {
    "width": width,
    "height": height,
    "current_x": 0,
    "current_y": 0,
    "multiple_x": 0,
    "multiple_y": 0
}


def gridify(data, grid):
  # print(data)
  for index, item in enumerate(grid):
    if item[0] == "vert":
      # print(item[1])
      copy = dict(data)

      copy["height"] = copy["height"] / len(item[1]) + 1
      copy["multiple_y"] = copy["height"] / len(item[1]) + 1
      copy["multiple_x"] = 0
      copy["current_y"] = copy["current_y"] + index * copy["multiple_y"]

      yield from gridify(copy, item[1])
    if item[0] == "hoz":
      copy = dict(data)
      copy["width"] = copy["width"] / (len(item[1]) + 1)
      copy["multiple_y"] = 0
      copy["multiple_x"] = copy["width"] / (len(item[1]) + 1)
      # print("in hoz", copy["multiple_x"])
      copy["current_x"] = copy["current_x"] + index * copy["multiple_x"]
      # print(item[1])
      yield from gridify(copy, item[1])
    if item[0] == "windows":

      for meindex, item in enumerate(item[1]):
        copy = dict(data)
        copy["current_y"] = copy["current_y"] + meindex * copy["multiple_y"]
        copy["current_x"] = copy["current_x"] + meindex * copy["multiple_x"]
        yield ("window", copy, item[1])


from pprint import pprint
for item in gridify(data, grid):
  pprint(item)


x = 0
end = width
for line in range(0, lines["max"]):
  # print(line)
  current_x = 0
  output = ""
  x = 0
  for item in gridify(data, grid):
    # pprint(item)
    limit = int(item[1]["current_x"])
    limitwidth = int(item[1]["width"])
    # print(limitwidth)
    nextdata = lines["windows"][item[2]][line][0:limitwidth].strip()
    # print("we took up ", len(nextdata))
    # print("we have to start at {}".format(limit))
    # print(limitwidth)
    output += (limit - x) * " "
    output += nextdata
    x += len(nextdata)
  print(output)
  