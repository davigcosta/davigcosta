extends Node3D

var robot: Node3D
var input: LineEdit
var output: RichTextLabel
var http: HTTPRequest

func _ready():
    _build_scene()

func _build_scene():
    var environment := WorldEnvironment.new()
    var env := Environment.new()
    env.background_mode = Environment.BG_COLOR
    env.background_color = Color("10182b")
    environment.environment = env
    add_child(environment)

    var light := DirectionalLight3D.new()
    light.rotation_degrees = Vector3(-35, -25, 0)
    light.light_energy = 1.2
    add_child(light)

    robot = MeshInstance3D.new()
    var mesh := BoxMesh.new()
    mesh.size = Vector3(1.5, 1.2, 1.0)
    robot.mesh = mesh
    robot.position = Vector3(0, 1.4, 0)
    var material := StandardMaterial3D.new()
    material.albedo_color = Color("49c6d8")
    robot.material_override = material
    add_child(robot)

    var camera := Camera3D.new()
    camera.position = Vector3(0, 2, 6)
    camera.look_at(Vector3(0, 1.2, 0))
    add_child(camera)

    var ui := CanvasLayer.new()
    add_child(ui)
    output = RichTextLabel.new()
    output.position = Vector2(30, 400)
    output.size = Vector2(940, 150)
    ui.add_child(output)
    input = LineEdit.new()
    input.position = Vector2(30, 580)
    input.size = Vector2(760, 40)
    input.placeholder_text = "Type in any language"
    ui.add_child(input)
    var button := Button.new()
    button.position = Vector2(810, 580)
    button.size = Vector2(120, 40)
    button.text = "Send"
    button.pressed.connect(send_message)
    ui.add_child(button)

func send_message():
    var message := input.text.strip_edges()
    if message.is_empty():
        return
    output.append_text("You: " + message + "\\n")
    input.clear()
    http = HTTPRequest.new()
    add_child(http)
    http.request_completed.connect(_on_response)
    http.request("http://127.0.0.1:8000/chat", ["Content-Type: application/json"], HTTPClient.METHOD_POST, JSON.stringify({"message": message}))

func _on_response(_result, _code, _headers, body):
    var data = JSON.parse_string(body.get_string_from_utf8())
    if data:
        output.append_text("Aurora (" + str(data.provider) + "): " + str(data.text) + "\\n")
