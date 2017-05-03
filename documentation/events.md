## Events

### Moved
```
{
	name: moved
	success: true/false
}
```

### Look
```
{
	name: look
	peeking: true/false
	room: string
	entities:
	[
		name,
	]
	items:
	[
		name,
	]
}
```

### Hear

note: this should get sent back to the speaker
```
{
	name: hear
	text: string
	speaker: player
}
```
