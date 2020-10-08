# geev_api
An unofficial api for geev.com/fr

## Installation

```bash
git clone https://github.com/bastienbourgeois/geev_api
```

## Usage

```python
from src.geev import Geev

geev = Geev('my_email@example.com', 'my_password')

location = getLocationFromAddress('5 Avenue Anatole France Paris')
geev.getObjects(1, location, 5000)
geev.getObjects(2, location, 5000)

geev.getConversation()
```

## License
[MIT](https://github.com/bastienbourgeois/geev_api/blob/main/LICENSE)
