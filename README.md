# SafeBox

<a href="https://discord.gg/xk5ZCxBVyh"><img src="https://discord.com/api/guilds/988721780317384794/widget.png?style=banner2"></a>

## safebox is a tools for create a portable encrypted disk.

## build and run

This project use poetry for dependency manager, so install poetry and run follow command:

```bash
poetry update
poetry shell
poetry build
poetry install
sudo python -m safebox
```

## Todo

- [X] Create SafeBox creator App
- [ ] Add logger
- [ ] Create unlock App
- [ ] Fix permission denied exception
- [ ] Add permission denied exception handler and show correct message in GUI
- [ ] Add theme selector
- [ ] Add installation documents.
- [ ] Add usage documents
- [ ] Add system try-icon for unlock App
- [ ] Add selected device information
- [ ] Show process indicator on creating the partition
- [ ] Show a message after creating the partition
- [ ] Change creates SafeBox bottom to open SafeBox after creating the partition
- [ ] Detect this device is SafeBox or not.
