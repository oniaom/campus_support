""" Creates the cards for resources/outlook page"""


class Creator:
    def __init__(self, id: int, card_title: str, image: dict, description: str, button_title: str, button_text: str) -> None:
        self.id = id
        self.card_title = card_title
        self.image = image
        self.descrciption = description
        self.button_title = button_title
        self.button_text = button_text

    def create_card(self) -> str:
        image_path = self.image["path"]
        image_alt = self.image["alt"]

        return f"""<li class="list-inline-item">
        <div class="card" style="width: 18rem;">
            <div class="card-body">
                <h5 class="card-title">{self.card_title}</h5>
                <img src="{{ url_for('static', filename='{image_path}')}}" class="card-img-top"
                alt="{image_alt}">
                <p class="card-text">{self.descrciption}</p>
                    <p>
                        <a class="btn btn-primary" data-bs-toggle="collapse" href="#collapse{self.id}" role="button" aria-expanded="false" aria-controls="collapseid{id}">
                        {self.button_title}
                        </a>
                      </p>
                      <div class="collapse" id="collapseid{id}">
                        <div class="card card-body">
                          {self.button_text}
                        </div>
                      </div>
            </div>
        </div>
    </li>"""
