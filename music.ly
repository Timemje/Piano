\version "2.24.0"

\header {
  title = "An Unfinished Grief"
  subtitle = "Concert Prelude for Solo Piano"
  subsubtitle = "in C-sharp minor"
  tagline = ##f
}

\paper {
  #(set-paper-size "a4")
  top-margin = 13\mm
  bottom-margin = 13\mm
  left-margin = 15\mm
  right-margin = 15\mm
  system-system-spacing = #'((basic-distance . 15) (minimum-distance . 11) (padding . 2.5) (stretchability . 12))
  markup-system-spacing.padding = #3
  ragged-last-bottom = ##t
  ragged-bottom = ##f
  print-first-page-number = ##f
  oddHeaderMarkup = \markup \fill-line { "" \unless \on-first-page \fromproperty #'page:page-number-string }
  evenHeaderMarkup = \markup \fill-line { \unless \on-first-page \fromproperty #'page:page-number-string "" }
}

#(set-global-staff-size 18.5)

global = { \key cis \minor \time 4/4 }

rightA = {
  % m.1
  \oneVoice r2 r4 r8 gis'8( |
  % m.2
  \oneVoice a'4.-- gis'8 e'2) |
  % m.3
  \voiceOne r8 e'8( fis' gis' b'4.-- a'8~ |
  % m.4
  \voiceOne a'4 gis'2) r4 |
  % m.5
  \voiceOne r4 r8 gis'8( a'4.-- gis'8 |
  % m.6
  \voiceOne e'4) r8 a'8( d''4.-- cis''8 |
  % m.7
  \voiceOne bis'4. cis''8 dis''4 bis'4 |
  % m.8
  \voiceOne cis''2.) r4 |
  % m.9
  \oneVoice r8 gis'8( a' b' e''4.-- dis''8 |
  % m.10
  \voiceOne cis''4 b'8 a'8 gis'4 fis'4) |
  % m.11
  \oneVoice r8 g'8( a' b' e''4.-- d''8 |
  % m.12
  \oneVoice cis''4 b'8 a'8 fisis'2) |
  % m.13
  \oneVoice gis'4( a'2.~ |
  % m.14
  \oneVoice a'4 gis'4 e'2) |
  % m.15
  \voiceOne r8 gis'8( a'4.-- gis'8 fis'8 e'8 |
  % m.16
  \voiceOne dis'2) r2\fermata |
  % m.17
  \voiceOne r8 gis'8( a'4.-- gis'8 e'4) |
  % m.18
  \voiceOne r8 bis'8( cis''4.-- bis'8 gis'4) |
  % m.19
  \voiceOne r8 dis''8( e''4.-- dis''8 b'4) |
  % m.20
  \voiceOne r8 fis''8( g''4.-- fis''8 d''4) |
  % m.21
  \voiceOne a''2.--( gis''4) |
  % m.22
  \voiceOne gis''2( fis''4 e''4) |
  % m.23
  \voiceOne r8 cis''8( d''4.-- cis''8 a'4) |
  % m.24
  \voiceOne gis'2( b'4. a'8) |
  % m.25
  \oneVoice gis'4( a'4.-- gis'8 eis'4) |
  % m.26
  \oneVoice r8 fis'8( gis' a' cis''4.-- b'8) |
  % m.27
  \voiceOne r8 <ais' ais''>8( <b' b''>4.-- <ais' ais''>8 <fisis' fisis''>4) |
  % m.28
  \voiceOne <gis' gis''>8( <ais' ais''> <b' b''> <cis'' cis'''> <dis'' dis'''>4.-- <cis'' cis'''>8) |
  % m.29
  \oneVoice <b' b''>8( <c'' c'''>4 <b' b''>8 <gis' gis''>4 <a' a''>4) |
  % m.30
  \oneVoice <e'' e'''>4( <f'' f'''>4.-- <e'' e'''>8 <cis'' cis'''>4) |
  % m.31
  \oneVoice <fis'' a'' d''' fis'''>2.->( <e'' a'' cis''' e'''>4) |
  % m.32
  \oneVoice <d'' f'' a'' d'''>2( <cis'' e'' g'' cis'''>4 <a' e'' g'' a''>4) |
  % m.33
  \voiceOne \key d \minor r8 a'8( bes'4.-- a'8 f'4) |
  % m.34
  \voiceOne r8 f'8( g' a' d''4.-- c''8) |
  % m.35
  \oneVoice r8 <d'' d'''>8( <ees'' ees'''>4.-- <d'' d'''>8 <bes' bes''>4) |
  % m.36
  \oneVoice r8 <a' a''>8( <bes' bes''>4) r8 <a' a''>8( <bes' bes''>4) |
  % m.37
  \oneVoice \key cis \minor <a' d'' f'' a''>4( <bes' d'' f'' bes''>4 <a' bis' dis'' a''>2) |
  % m.38
  \oneVoice <gis' cis'' e'' gis''>4.( <a' a''>8 <b' d'' eis'' b''>2) |
  % m.39
  \oneVoice <a' cis'' fis'' a''>4.( <b' b''>8 <cis'' e'' ais'' cis'''>2) |
  % m.40
  \oneVoice <bis' dis'' fis'' bis''>4( <dis'' fis'' a'' dis'''>4 <fis'' a'' bis'' fis'''>4.) <gis'' gis'''>8( |
  % m.41
  \oneVoice \ottava #1 <a'' e''' gis''' a'''>4.-> <gis'' cis''' e''' gis'''>8 <e'' gis'' cis''' e'''>2~) |
  % m.42
  \oneVoice <e'' gis'' cis''' e'''>2. <e'' a'' b'' cis''' e'''>4 |
  % m.43
  \oneVoice <a'' bis'' dis''' a'''>4->( <gis'' bis'' dis''' gis'''>2.) |
  % m.44
  \oneVoice \ottava #0 r4 r8 <gis' gis''>8( <a' cis'' e'' a''>4.-> <gis' cis'' e'' gis''>8 |
  % m.45
  \oneVoice <e' a' cis'' e''>4) r8 <a' a''>8( <d'' fis'' a'' d'''>4.-> <cis'' cis'''>8) |
  % m.46
  \oneVoice <bis' dis'' gis'' bis''>4.( <cis'' cis'''>8 <dis'' fis'' bis'' dis'''>4 <bis' dis'' gis'' bis''>4) |
  % m.47
  \oneVoice <dis'' fis'' bis'' dis'''>4.( <e'' gis'' bis'' e'''>8 <fis'' bis'' dis''' fis'''>4 <dis'' fis'' bis'' dis'''>4) |
  % m.48
  \oneVoice \ottava #1 <fis'' a'' bis'' fis'''>4.( <gis'' bis'' dis''' gis'''>8 <a'' bis'' dis''' a'''>4 <fis'' a'' bis'' fis'''>4) |
  % m.49
  \oneVoice <a'' bis'' dis''' a'''>4.( <bis'' dis''' fis''' bis'''>8 <cis''' e''' a''' cis''''>4 <a'' dis''' fis''' a'''>4) |
  % m.50
  \oneVoice <a'' bis'' dis''' fis''' a'''>1-> \breathe |
  % m.51
  \oneVoice <gis'' a'' cis''' e''' gis'''>1-> |
  % m.52
  \oneVoice <fisis'' a'' cis''' e''' fisis'''>2-> \ottava #0 <e'' e'''>8( <cis'' cis'''> <a' a''> <fisis' fisis''>) |
  % m.53
  \oneVoice <e' e''>8( <cis' cis''> <bis bis'> <gis gis'>) <gis bis dis' gis'>2 |
  % m.54
  \oneVoice R1 |
  % m.55
  \oneVoice r2 r8 a''8(-- gis''4) |
  % m.56
  \oneVoice r2 r2\fermata |
  % m.57
  \oneVoice r2 gis'2( |
  % m.58
  \oneVoice a'1~ |
  % m.59
  \oneVoice a'2) r2 |
  % m.60
  \oneVoice r2 r4 r8 gis'8( |
  % m.61
  \oneVoice a'4.-- gis'8 e'2) |
  % m.62
  \voiceOne r8 e'8( fis' gis' b'4.-- a'8~ |
  % m.63
  \voiceOne a'4 gis'2) r4 |
  % m.64
  \voiceOne r4 r8 gis'8( a'4.-- gis'8 |
  % m.65
  \voiceOne e'4) r8 a'8( d''2) |
  % m.66
  \voiceOne cis''2( bis'2) |
  % m.67
  \oneVoice r2\fermata r2 |
  % m.68
  \oneVoice r4 gis''2(-- fisis''4 |
  % m.69
  \oneVoice gis''2) r2 |
  % m.70
  \oneVoice r8 e'8( fis'8 gis'8~ gis'2) |
  % m.71
  \voiceOne gis'1~ |
  % m.72
  \voiceOne gis'2 r2 |
  % m.73
  \voiceOne r8 gis'8( a'4.-- gis'8) r4 |
  % m.74
  \oneVoice r2 r8 gis'8( a'4~ |
  % m.75
  \oneVoice a'2) r2 |
  % m.76
  \oneVoice R1 |
  % m.77
  \oneVoice r2 r4 a'4~( |
  % m.78
  \oneVoice a'2 gis'2)~ |
  % m.79
  \oneVoice gis'1~ |
  % m.80
  \oneVoice gis'2\fermata r2\fermata |
}

rightB = {
  % m.1
  s1 |
  % m.2
  s1 |
  % m.3
  \voiceTwo s2 <cis' e'>2 |
  % m.4
  \voiceTwo <bis dis'>2 <bis fis'>4 s4 |
  % m.5
  \voiceTwo s4 <cis' e'>2. |
  % m.6
  \voiceTwo cis'2 <fis' a'>2 |
  % m.7
  \voiceTwo <dis' fis'>1 |
  % m.8
  \voiceTwo e'2 a'4( gis'4) |
  % m.9
  s1 |
  % m.10
  \voiceTwo s2 e'4 <a dis'>4 |
  % m.11
  s1 |
  % m.12
  s1 |
  % m.13
  s1 |
  % m.14
  s1 |
  % m.15
  \voiceTwo <bis dis'>2 <bis d'>2 |
  % m.16
  \voiceTwo bis2 s2 |
  % m.17
  \voiceTwo <cis' e'>2. s4 |
  % m.18
  \voiceTwo <dis' fis'>2. fis'4~ |
  % m.19
  \voiceTwo fis'2 a'2~ |
  % m.20
  \voiceTwo a'2. s4 |
  % m.21
  \voiceTwo <dis'' fis''>2. <bis' dis''>4 |
  % m.22
  \voiceTwo <cis'' e''>2 <a' cis''>2 |
  % m.23
  \voiceTwo <fis' a'>2. s4 |
  % m.24
  \voiceTwo <cis' e'>2. s4 |
  % m.25
  s1 |
  % m.26
  s1 |
  % m.27
  \voiceTwo s8 cis''2.. |
  % m.28
  \voiceTwo b'8 s8 s2. |
  % m.29
  s1 |
  % m.30
  s1 |
  % m.31
  s1 |
  % m.32
  s1 |
  % m.33
  \voiceTwo d'2( cis'2) |
  % m.34
  \voiceTwo c'2 f'2 |
  % m.35
  s1 |
  % m.36
  s1 |
  % m.37
  s1 |
  % m.38
  s1 |
  % m.39
  s1 |
  % m.40
  s1 |
  % m.41
  s1 |
  % m.42
  s1 |
  % m.43
  s1 |
  % m.44
  s1 |
  % m.45
  s1 |
  % m.46
  s1 |
  % m.47
  s1 |
  % m.48
  s1 |
  % m.49
  s1 |
  % m.50
  s1 |
  % m.51
  s1 |
  % m.52
  s1 |
  % m.53
  s1 |
  % m.54
  s1 |
  % m.55
  s1 |
  % m.56
  s1 |
  % m.57
  s1 |
  % m.58
  s1 |
  % m.59
  s1 |
  % m.60
  s1 |
  % m.61
  s1 |
  % m.62
  \voiceTwo s2 <c' e'>2 |
  % m.63
  \voiceTwo <b d'>2 <b fis'>4 s4 |
  % m.64
  \voiceTwo s4 <cis' e'>4 <dis' fis'>2 |
  % m.65
  \voiceTwo cis'2 fis'2 |
  % m.66
  \voiceTwo <e' a'>2 <dis' fis'>2 |
  % m.67
  s1 |
  % m.68
  s1 |
  % m.69
  s1 |
  % m.70
  s1 |
  % m.71
  \voiceTwo <bis dis'>2 <bis d'>2 |
  % m.72
  \voiceTwo <b d'>2 s2 |
  % m.73
  \voiceTwo s4 <d' f'>4( cis'4) s4 |
  % m.74
  s1 |
  % m.75
  s1 |
  % m.76
  s1 |
  % m.77
  s1 |
  % m.78
  s1 |
  % m.79
  s1 |
  % m.80
  s1 |
}

leftA = {
  % m.1
  \oneVoice <cis,, cis,>1 |
  % m.2
  \oneVoice r2 <e gis cis'>2~ |
  % m.3
  \oneVoice <e gis cis'>2 <a,, a,>2 |
  % m.4
  \oneVoice <gis,, gis,>2. r4 |
  % m.5
  \oneVoice <cis, gis,>2 b,,2 |
  % m.6
  \oneVoice a,,2 fis,2 |
  % m.7
  \oneVoice <gis,, gis,>1 |
  % m.8
  \oneVoice <a,, a,>1 |
  % m.9
  \oneVoice gis,4 <e b>2. |
  % m.10
  \oneVoice a,4 <e cis'>4 <b, fis>2 |
  % m.11
  \oneVoice g,4 r8 <e b>8~ <e b>2 |
  % m.12
  \oneVoice a,4 <e cis'>2. |
  % m.13
  \oneVoice <gis, cis e>4 <gis, bis, dis fis>2.~ |
  % m.14
  \oneVoice <gis, bis, dis fis>1 |
  % m.15
  \oneVoice <gis,, gis,>1~ |
  % m.16
  \oneVoice <gis,, gis,>2 r2\fermata |
  % m.17
  \oneVoice <cis, cis>4 e8( fis gis4 a4) |
  % m.18
  \oneVoice <bis,, bis,>4 dis8( e fis4 gis4) |
  % m.19
  \oneVoice <b,, b,>4 fis8( a dis'4. cis'8) |
  % m.20
  \oneVoice <fis,, fis,>2 a,8( d fis a) |
  % m.21
  \oneVoice <gis,, gis,>4 bis,8( dis fis4 a4) |
  % m.22
  \oneVoice <a,, a,>4 r8 gis8( a4.-- gis8) |
  % m.23
  \oneVoice <fis, e>1 |
  % m.24
  \oneVoice e,4 b,8( cis gis2) |
  % m.25
  \oneVoice <eis, eis>4 gis8( b cis' b gis b) |
  % m.26
  \oneVoice <fis, fis>4 a8( cis' e' cis' a cis') |
  % m.27
  \oneVoice <fisis, fisis>4 ais8( cis' dis' cis' ais cis') |
  % m.28
  \oneVoice <gis, gis>4 b8( dis' fis' dis' b dis') |
  % m.29
  \oneVoice <gis, gis>8( d' e'4) <a, a>8( cis' e'4) |
  % m.30
  \oneVoice <a,, a,>4 <e a cis'>4 <g,, g,>4 <e a cis'>4 |
  % m.31
  \oneVoice <fis,, fis,>4 a,8( d fis a d'4) |
  % m.32
  \oneVoice <d, d>2 <a,, a,>2 |
  % m.33
  \oneVoice \key d \minor d,16( a, d f a f d a, d, a, d f a f d a,) |
  % m.34
  \oneVoice d,16( a, c f a f c a, bes,, f, bes, d f d bes, f,) |
  % m.35
  \oneVoice g,,16( d, g, bes, d g d bes, ees, bes, ees g bes g ees bes,) |
  % m.36
  \oneVoice a,,16( e, a, cis e g e cis a,, e, g, cis e g bes g) |
  % m.37
  \oneVoice \key cis \minor <d, d>8 f <a d'>4 <dis, dis>8 fis <a bis>4 |
  % m.38
  \oneVoice <e, e>8 gis <cis' e'>4 <eis, eis>8 gis <b d'>4 |
  % m.39
  \oneVoice <fis, fis>8 a <cis' fis'>4 <fisis, fisis>8 ais <cis' e'>4 |
  % m.40
  \oneVoice <gis,, gis,>8 dis gis bis dis' fis' r4 |
  % m.41
  \oneVoice <cis,, cis,>4-> gis,8( cis e gis e cis) |
  % m.42
  \oneVoice r8 <e, e>8(-> <fis, fis> <gis, gis> <b, b>4-> <a, a>4) |
  % m.43
  \oneVoice <gis,, gis,>4 dis8( gis bis dis' fis'4) |
  % m.44
  \oneVoice <b,, b,>4 <e gis cis'>4 <a,, a,>4 <e a cis'>4 |
  % m.45
  \oneVoice <a,, a,>4 <e a cis'>4 <fis,, fis,>4 <a d' fis'>4 |
  % m.46
  \oneVoice \tuplet 3/2 { <gis,, gis,>8 dis gis } \tuplet 3/2 { bis gis dis } \tuplet 3/2 { <gis,, gis,>8 dis gis } \tuplet 3/2 { bis gis dis } |
  % m.47
  \oneVoice \tuplet 3/2 { <gis,, gis,>8 dis fis } \tuplet 3/2 { bis fis dis } \tuplet 3/2 { <gis,, gis,>8 dis fis } \tuplet 3/2 { bis fis dis } |
  % m.48
  \oneVoice gis,,16( gis, dis gis, gis,, gis, dis gis, gis,, gis, fis gis, gis,, gis, fis gis,) |
  % m.49
  \oneVoice gis,,16( gis, dis gis, gis,, gis, fis gis, gis,, gis, a gis, gis,, gis, a gis,) |
  % m.50
  \oneVoice <gis,, gis,>4-> \tuplet 3/2 { bis8 dis' fis' } \tuplet 3/2 { dis' bis gis } \tuplet 3/2 { dis bis, gis, } |
  % m.51
  \oneVoice <a,,, a,,>4-> <e a cis' e'>2. |
  % m.52
  \oneVoice <a,, a,>2 r2 |
  % m.53
  \oneVoice r2 <gis,, gis,>2 |
  % m.54
  \oneVoice r8 <gis,, gis,>8( <a,, a,>4.-- <gis,, gis,>8 <e,, e,>4) |
  % m.55
  \oneVoice <gis,, gis,>1~ |
  % m.56
  \oneVoice <gis,, gis,>2 r2\fermata |
  % m.57
  \oneVoice <cis,, cis,>1 |
  % m.58
  \oneVoice r2 gis2~ |
  % m.59
  \oneVoice gis4 fisis4( gis2) |
  % m.60
  \oneVoice <cis,, cis,>1 |
  % m.61
  \oneVoice r4 <d f>4( <cis e>2) |
  % m.62
  \oneVoice <cis e>2 <a,, a,>2 |
  % m.63
  \oneVoice <gis,, gis,>2. r4 |
  % m.64
  \oneVoice <cis, gis,>2 <bis,, bis,>2 |
  % m.65
  \oneVoice b,,2 ais,,2 |
  % m.66
  \oneVoice a,,2 gis,,2 |
  % m.67
  \oneVoice r2\fermata a4(-- gis4) |
  % m.68
  \oneVoice <cis,, cis,>1 |
  % m.69
  \oneVoice R1 |
  % m.70
  \oneVoice <cis, gis,>2 <a, e>2 |
  % m.71
  \oneVoice <gis,, gis,>1~ |
  % m.72
  \oneVoice <gis,, gis,>2 r2 |
  % m.73
  \oneVoice <cis,, cis,>1 |
  % m.74
  \oneVoice <cis, gis,>2. r4 |
  % m.75
  \oneVoice R1 |
  % m.76
  \oneVoice <cis,, cis,>1 |
  % m.77
  \oneVoice R1 |
  % m.78
  \oneVoice R1 |
  % m.79
  \oneVoice <cis, gis,>1~ |
  % m.80
  \oneVoice <cis, gis,>2\fermata r2\fermata |
}

leftB = {
  % m.1
  s1 |
  % m.2
  s1 |
  % m.3
  s1 |
  % m.4
  s1 |
  % m.5
  s1 |
  % m.6
  s1 |
  % m.7
  s1 |
  % m.8
  s1 |
  % m.9
  s1 |
  % m.10
  s1 |
  % m.11
  s1 |
  % m.12
  s1 |
  % m.13
  s1 |
  % m.14
  s1 |
  % m.15
  s1 |
  % m.16
  s1 |
  % m.17
  s1 |
  % m.18
  s1 |
  % m.19
  s1 |
  % m.20
  s1 |
  % m.21
  s1 |
  % m.22
  s1 |
  % m.23
  s1 |
  % m.24
  s1 |
  % m.25
  s1 |
  % m.26
  s1 |
  % m.27
  s1 |
  % m.28
  s1 |
  % m.29
  s1 |
  % m.30
  s1 |
  % m.31
  s1 |
  % m.32
  s1 |
  % m.33
  s1 |
  % m.34
  s1 |
  % m.35
  s1 |
  % m.36
  s1 |
  % m.37
  s1 |
  % m.38
  s1 |
  % m.39
  s1 |
  % m.40
  s1 |
  % m.41
  s1 |
  % m.42
  s1 |
  % m.43
  s1 |
  % m.44
  s1 |
  % m.45
  s1 |
  % m.46
  s1 |
  % m.47
  s1 |
  % m.48
  s1 |
  % m.49
  s1 |
  % m.50
  s1 |
  % m.51
  s1 |
  % m.52
  s1 |
  % m.53
  s1 |
  % m.54
  s1 |
  % m.55
  s1 |
  % m.56
  s1 |
  % m.57
  s1 |
  % m.58
  s1 |
  % m.59
  s1 |
  % m.60
  s1 |
  % m.61
  s1 |
  % m.62
  s1 |
  % m.63
  s1 |
  % m.64
  s1 |
  % m.65
  s1 |
  % m.66
  s1 |
  % m.67
  s1 |
  % m.68
  s1 |
  % m.69
  s1 |
  % m.70
  s1 |
  % m.71
  s1 |
  % m.72
  s1 |
  % m.73
  s1 |
  % m.74
  s1 |
  % m.75
  s1 |
  % m.76
  s1 |
  % m.77
  s1 |
  % m.78
  s1 |
  % m.79
  s1 |
  % m.80
  s1 |
}

marks = {
  % m.1
  \tempo "Largo doloroso" 4 = 56 s1 |
  % m.2
  s1 |
  % m.3
  s1 |
  % m.4
  s1 |
  % m.5
  \break s1 |
  % m.6
  s1 |
  % m.7
  s1 |
  % m.8
  s1 |
  % m.9
  \break s1 |
  % m.10
  s1 |
  % m.11
  s1 |
  % m.12
  s1 |
  % m.13
  \break s1 |
  % m.14
  s1 |
  % m.15
  s1 |
  % m.16
  s1 |
  % m.17
  \pageBreak \tempo "Poco più mosso" 4 = 62 s1 |
  % m.18
  s1 |
  % m.19
  s1 |
  % m.20
  s1 |
  % m.21
  \break s1 |
  % m.22
  s1 |
  % m.23
  s1 |
  % m.24
  s1 |
  % m.25
  \break s1^"poco a poco animando" |
  % m.26
  s1 |
  % m.27
  s1 |
  % m.28
  s1 |
  % m.29
  \break s1 |
  % m.30
  s1 |
  % m.31
  s1 |
  % m.32
  s1 \bar "||" |
  % m.33
  \break \tempo "Più agitato" s1 |
  % m.34
  s1 |
  % m.35
  s1 |
  % m.36
  s1 \bar "||" |
  % m.37
  \break s1 |
  % m.38
  s1 |
  % m.39
  s1 |
  % m.40
  s2 s2^"allargando" |
  % m.41
  \break \tempo "Largamente, con tutta la forza" s1 |
  % m.42
  s1 |
  % m.43
  s1 |
  % m.44
  \break s4 s2.^"agitato" |
  % m.45
  s1 |
  % m.46
  s1^"stringendo poco a poco" |
  % m.47
  \break s1 |
  % m.48
  s1 |
  % m.49
  s2 s2^"allargando molto" |
  % m.50
  \break s1 |
  % m.51
  s1^"molto largo" |
  % m.52
  \break s2 s2^"smorzando" |
  % m.53
  s1 |
  % m.54
  \pageBreak s1^"Lento" |
  % m.55
  s1 |
  % m.56
  s1 |
  % m.57
  \break \tempo "Tempo I" s1 |
  % m.58
  s1 |
  % m.59
  s1 |
  % m.60
  s1 |
  % m.61
  \break s1 |
  % m.62
  s1 |
  % m.63
  s1 |
  % m.64
  s1 |
  % m.65
  \break s1 |
  % m.66
  s1 |
  % m.67
  s1 |
  % m.68
  s1 |
  % m.69
  \break s1 |
  % m.70
  s1 |
  % m.71
  s1 |
  % m.72
  s1 |
  % m.73
  \pageBreak s1^"Più lento" |
  % m.74
  s1 |
  % m.75
  s1 |
  % m.76
  s1 |
  % m.77
  \break s1 |
  % m.78
  s1 |
  % m.79
  s1 |
  % m.80
  s1 |
  \bar "|."
}

dyns = {
  % m.1
  s1\pp_"una corda" |
  % m.2
  s1 |
  % m.3
  s4 s4\< s4\> s4\! |
  % m.4
  s1 |
  % m.5
  s1\p |
  % m.6
  s4 s4\< s4\> s4 |
  % m.7
  s4\! s2. |
  % m.8
  s1\pp |
  % m.9
  s1\p-"dolce" |
  % m.10
  s2 s2\> |
  % m.11
  s1\pp |
  % m.12
  s4\< s4 s4\! s4 |
  % m.13
  s1\p |
  % m.14
  s2 s2\> |
  % m.15
  s1\pp |
  % m.16
  s2\> s2\! |
  % m.17
  s1\p |
  % m.18
  s1\< |
  % m.19
  s1 |
  % m.20
  s1 |
  % m.21
  s2.\mf s4\> |
  % m.22
  s1 |
  % m.23
  s1\p |
  % m.24
  s1\> |
  % m.25
  s1\p_"tre corde" |
  % m.26
  s1\< |
  % m.27
  s1 |
  % m.28
  s1 |
  % m.29
  s1\mf\< |
  % m.30
  s1 |
  % m.31
  s1\f |
  % m.32
  s1\> |
  % m.33
  s1\mp |
  % m.34
  s1\< |
  % m.35
  s1\mf |
  % m.36
  s1\p-"subito" |
  % m.37
  s1\< |
  % m.38
  s1\mf\< |
  % m.39
  s1\f\< |
  % m.40
  s1\ff |
  % m.41
  s1\ff |
  % m.42
  s1 |
  % m.43
  s1 |
  % m.44
  s4\f s2.\< |
  % m.45
  s1\ff |
  % m.46
  s1 |
  % m.47
  s1\< |
  % m.48
  s1 |
  % m.49
  s1\< |
  % m.50
  s1\fff |
  % m.51
  s1\fff |
  % m.52
  s2\ff s2\> |
  % m.53
  s2 s2\p |
  % m.54
  s1\pp |
  % m.55
  s2 s2\ppp |
  % m.56
  s1 |
  % m.57
  s1\pp_"una corda" |
  % m.58
  s1 |
  % m.59
  s1 |
  % m.60
  s1\p |
  % m.61
  s1\mp |
  % m.62
  s4 s4\< s4\> s4\! |
  % m.63
  s1\p |
  % m.64
  s1 |
  % m.65
  s4 s4\< s2\! |
  % m.66
  s1\> |
  % m.67
  s2 s2\pp |
  % m.68
  s1 |
  % m.69
  s2 s2\ppp |
  % m.70
  s1\pp |
  % m.71
  s1 |
  % m.72
  s2\> s2\! |
  % m.73
  s1\pp |
  % m.74
  s1 |
  % m.75
  s1 |
  % m.76
  s1\ppp |
  % m.77
  s1-"morendo" |
  % m.78
  s1 |
  % m.79
  s1 |
  % m.80
  s1 |
}

peds = {
  \set Dynamics.pedalSustainStyle = #'mixed
  % m.1
  s1\sustainOn |
  % m.2
  s2 s2\sustainOff\sustainOn |
  % m.3
  s2 s2\sustainOff\sustainOn |
  % m.4
  s2.\sustainOff\sustainOn s4\sustainOff |
  % m.5
  s2\sustainOn s2\sustainOff\sustainOn |
  % m.6
  s2\sustainOff\sustainOn s2\sustainOff\sustainOn |
  % m.7
  s2\sustainOff\sustainOn s2\sustainOff\sustainOn |
  % m.8
  s2\sustainOff\sustainOn s4\sustainOff\sustainOn s4\sustainOff\sustainOn |
  % m.9
  s2\sustainOff\sustainOn s2\sustainOff\sustainOn |
  % m.10
  s4\sustainOff\sustainOn s4 s4\sustainOff\sustainOn s4\sustainOff\sustainOn |
  % m.11
  s2\sustainOff\sustainOn s2\sustainOff\sustainOn |
  % m.12
  s4\sustainOff\sustainOn s4 s2\sustainOff\sustainOn |
  % m.13
  s4\sustainOff\sustainOn s2.\sustainOff\sustainOn |
  % m.14
  s4\sustainOff\sustainOn s4\sustainOff\sustainOn s2\sustainOff\sustainOn |
  % m.15
  s2\sustainOff\sustainOn s2\sustainOff\sustainOn |
  % m.16
  s2 s2\sustainOff |
  % m.17
  s2\sustainOn s2\sustainOff\sustainOn |
  % m.18
  s2\sustainOff\sustainOn s2\sustainOff\sustainOn |
  % m.19
  s2\sustainOff\sustainOn s2\sustainOff\sustainOn |
  % m.20
  s2\sustainOff\sustainOn s2\sustainOff\sustainOn |
  % m.21
  s2\sustainOff\sustainOn s4 s4\sustainOff\sustainOn |
  % m.22
  s2\sustainOff\sustainOn s2\sustainOff\sustainOn |
  % m.23
  s2\sustainOff\sustainOn s2\sustainOff\sustainOn |
  % m.24
  s1\sustainOff\sustainOn |
  % m.25
  s2\sustainOff\sustainOn s2\sustainOff\sustainOn |
  % m.26
  s2\sustainOff\sustainOn s2\sustainOff\sustainOn |
  % m.27
  s2\sustainOff\sustainOn s2\sustainOff\sustainOn |
  % m.28
  s2\sustainOff\sustainOn s2\sustainOff\sustainOn |
  % m.29
  s2\sustainOff\sustainOn s2\sustainOff\sustainOn |
  % m.30
  s2\sustainOff\sustainOn s2\sustainOff\sustainOn |
  % m.31
  s2.\sustainOff\sustainOn s4\sustainOff\sustainOn |
  % m.32
  s2\sustainOff\sustainOn s2\sustainOff\sustainOn |
  % m.33
  s2\sustainOff\sustainOn s2\sustainOff\sustainOn |
  % m.34
  s2\sustainOff\sustainOn s2\sustainOff\sustainOn |
  % m.35
  s2\sustainOff\sustainOn s2\sustainOff\sustainOn |
  % m.36
  s2\sustainOff\sustainOn s2\sustainOff\sustainOn |
  % m.37
  s2\sustainOff\sustainOn s2\sustainOff\sustainOn |
  % m.38
  s2\sustainOff\sustainOn s2\sustainOff\sustainOn |
  % m.39
  s2\sustainOff\sustainOn s2\sustainOff\sustainOn |
  % m.40
  s1\sustainOff\sustainOn |
  % m.41
  s2\sustainOff\sustainOn s2\sustainOff\sustainOn |
  % m.42
  s2 s4\sustainOff\sustainOn s4\sustainOff\sustainOn |
  % m.43
  s1\sustainOff\sustainOn |
  % m.44
  s2\sustainOff\sustainOn s2\sustainOff\sustainOn |
  % m.45
  s2\sustainOff\sustainOn s2\sustainOff\sustainOn |
  % m.46
  s1\sustainOff\sustainOn |
  % m.47
  s2\sustainOff\sustainOn s2\sustainOff\sustainOn |
  % m.48
  s2\sustainOff\sustainOn s2\sustainOff\sustainOn |
  % m.49
  s2\sustainOff\sustainOn s2\sustainOff\sustainOn |
  % m.50
  s1\sustainOff\sustainOn |
  % m.51
  s1\sustainOff\sustainOn |
  % m.52
  s1\sustainOff\sustainOn |
  % m.53
  s2\sustainOff\sustainOn s2\sustainOff\sustainOn |
  % m.54
  s1\sustainOff |
  % m.55
  s1\sustainOn |
  % m.56
  s2 s2\sustainOff |
  % m.57
  s1\sustainOn |
  % m.58
  s1 |
  % m.59
  s4\sustainOff\sustainOn s4\sustainOff\sustainOn s2\sustainOff\sustainOn |
  % m.60
  s1\sustainOff\sustainOn |
  % m.61
  s2 s2\sustainOff\sustainOn |
  % m.62
  s2 s2\sustainOff\sustainOn |
  % m.63
  s2.\sustainOff\sustainOn s4\sustainOff |
  % m.64
  s2\sustainOn s2\sustainOff\sustainOn |
  % m.65
  s2\sustainOff\sustainOn s2\sustainOff\sustainOn |
  % m.66
  s2\sustainOff\sustainOn s2\sustainOff\sustainOn |
  % m.67
  s2\sustainOff s2\sustainOn |
  % m.68
  s1\sustainOff\sustainOn |
  % m.69
  s1 |
  % m.70
  s2\sustainOff\sustainOn s2\sustainOff\sustainOn |
  % m.71
  s2\sustainOff\sustainOn s2\sustainOff\sustainOn |
  % m.72
  s2\sustainOff\sustainOn s2\sustainOff |
  % m.73
  s1\sustainOn |
  % m.74
  s1\sustainOff\sustainOn |
  % m.75
  s1 |
  % m.76
  s1\sustainOff\sustainOn |
  % m.77
  s1 |
  % m.78
  s2 s2\sustainOff\sustainOn |
  % m.79
  s1\sustainOff\sustainOn |
  % m.80
  s2 s2\sustainOff |
}


\score {
  \new PianoStaff <<
    \new Staff = "up" <<
      \global
      \new Voice = "RA" \rightA
      \new Voice = "RB" \rightB
      \new Voice = "MK" \marks
    >>
    \new Dynamics \dyns
    \new Staff = "down" <<
      \global
      \clef bass
      \new Voice = "LA" \leftA
      \new Voice = "LB" \leftB
    >>
    \new Dynamics \peds
  >>

  \layout {
    \context {
      \Score
      \override SpacingSpanner.base-shortest-duration = #(ly:make-moment 1/16)
      \override MetronomeMark.padding = #2
      \override BarNumber.break-visibility = #end-of-line-invisible
      barNumberVisibility = #first-bar-number-invisible-save-broken-bars
    }
    \context {
      \PianoStaff
      \override StaffGrouper.staff-staff-spacing = #'((basic-distance . 12) (minimum-distance . 8) (padding . 2) (stretchability . 6))
    }
    \context {
      \Dynamics
      \override TextScript.font-shape = #'italic
      \override DynamicLineSpanner.staff-padding = #1.5
    }
    \context {
      \Voice
      \override TextScript.font-shape = #'italic
      \override BreathingSign.text = \markup \musicglyph "scripts.caesura.straight"
      
    }
  }
}
