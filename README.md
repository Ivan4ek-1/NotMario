Игра: NotMario

Описание: Программа будет представлять из себя платформер, похожий на Марио с несколькими уровнями. Цель игры - получить максимально много очков, пройти все уровни. Игра будет написана на языке программирования Python с использованием внутриязыковых модулей.

Tехническое задание
В игре должно присутствовать:
1. Главное меню с выбором уровней
2. Счетчик очков за пройденный уровень
3. Подбираемые предметы - монеты
4. Экран поражения с результатами
5. Усложнения геймплея по типу плавающих платформ и потайных комнат
6. Спрайты обьектов, игрока и врагов
7. Механики столкновения игрока с врагами, обьектами
8. База данных для хранения результатов игроков

Пояснительная записка
Название: Подделка Марио
Автор: Земзеров Иван

Описание идеи:
Игра, представляющая собой платформер, в котором нужно собрать максимальное количество очков и дойти до конца уровня.

Описание реализации:
Модель игрока написана классом, как и все объекты в игре, для того чтобы столкновение спрайтов было легче реализовать и чтобы код выглядел структурировано.
Подсчет очков в игре начинается с 1000 очков и со временем падает, чтобы игрок не задерживался надолго, за прохождение уровня начисляются дополнительные очки.
Для начального и конечного экрана используются дополнительные игровые циклы.

Технологии:
Pygame - модуль, на которм написана игра
Sys - вспомогательный модуль для выхода из игры
Os - модуль для подключения изображений спрайтов

презентация: https://docs.google.com/presentation/d/18zVEGL02lun3neQQOvQK_Yt5JFieXjOG/edit?usp=sharing&ouid=107775468984544918850&rtpof=true&sd=true
