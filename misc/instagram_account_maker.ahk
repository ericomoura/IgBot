#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
; #Warn  ; Enable warnings to assist with detecting common errors.
SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.

random_alphanumeric(){
	alphanumeric := ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

	Random, rng, 1, alphanumeric.length()
	return alphanumeric[rng]
}

generate_alias(){
	Loop 10{
		alias .= random_alphanumeric()
	}
	return alias
}

random_first_name(){
	first_names := ["Rodrigo", "Erico", "Matheus", "Mateus", "Pablo", "Guilherme", "Vitor", "Ronaldo", "Caio", "Catarina", "Maria", "Luisa", "Fernanda", "Fernando", "Joao", "John", "Mike", "Chris", "Layla", "Mary", "Gunther", "Leonard", "Mark"]
    Random, rng, 1, first_names.length()
    return first_names[rng]
}

random_last_name(){
 	last_names := ["Moura", "Ferreira", "Terry", "Cortez", "Marques", "Smith", "Ferraz", "Barbieri", "Panho", "Lima", "Williams", "Jones", "Brown", "Davis", "Miller", "Coimbra", "Schmidt", "Schneider", "Weber", "Maia"]
   	Random, rng, 1, last_names.length()
   	return last_names[rng]
}

^!+b::
Sleep 1000

;Account details
email := "EMAIL HERE+" . generate_alias() . "@mail.com"
first_name := random_first_name()
last_name := random_last_name()
name := first_name . " " . last_name
Random, rng, 0, 9999
username := Format("{:L}{:L}{:i}", first_name, last_name, rng)
password := "PASSWORD HERE"

;Opens Firefox
Send, #r
Sleep 250
Send, firefox -private-window{Enter}
Sleep 2000

;Signs up for Instagram
Send ^l
Sleep 200
Send, https://www.instagram.com/{Enter}
Sleep 6000

;Send, {Tab}{Tab}{Enter} ;Cookies popup

Send, {Tab}{Tab} ;Navigates to e-mail field
SendRaw, %email% ;Pastes e-mail

Send, {Tab} ;Navigates to name field
SendRaw, %name% ;Pastes name

Send, {Tab} ;Navigates to username field
SendRaw, %username% ;Pastes username

Send, {Tab} ;Navigates to password field
SendRaw, %password% ;Pastes password

Send, {Tab}{Tab}{Enter}	;Sign up
Sleep, 5000
return


+Esc::
ExitApp
return