const API_BASE_URL = "http://localhost:8000/api";
/* ==================== CONSTANTS ==================== */
const HOBBIES = [
  { id: 'drawing', name: 'рисование', icon: '✏️' },
  { id: 'knitting', name: 'вязание', icon: '🧶' },
  { id: 'running', name: 'бег', icon: '🏃' },
  { id: 'gardening', name: 'садоводство', icon: '🌱' },
  { id: 'dancing', name: 'танцы', icon: '💃' },
  { id: 'tourism', name: 'туризм', icon: '🏕️' },
  { id: 'cooking', name: 'кулинария', icon: '🍳' },
  { id: 'sculpting', name: 'лепка', icon: '🐻' },
  { id: 'singing', name: 'пение', icon: '🎤' },
  { id: 'sport', name: 'спорт', icon: '⚽' },
  { id: 'collecting', name: 'коллекционирование', icon: '🗂️' },
  { id: 'photography', name: 'фотография', icon: '📷' },
  { id: 'music', name: 'музыка', icon: '🎵' },
  { id: 'instruments', name: 'игра на муз. инструментах', icon: '🎸' },
  { id: 'volunteering', name: 'волонтёрство', icon: '🤝' },
  { id: 'reading', name: 'чтение', icon: '📖' },
];
const LEVELS = ['Новичок', 'Любитель', 'Профи', 'Продолжительный'];
const GOAL_HINTS = ['Освоить новую технику','Найти единомышленников','Участвовать в выставке','Развить творческие навыки','Прочитать 20 книг за год','Освоить новую профессию'];
const SUGGESTED_TAGS = ['#Хобби','#Советы','#Новичок','#Профи','#Вязание','#Рисование','#Садоводство','#Бег','#Кулинария','#Лепка','#Музыка','#Фото'];

const ALL_USERS = [
  { id: 1, name: 'ПурПурПур', avatar: 'https://images.unsplash.com/photo-1570295999919-56ceb5ecca61?w=100', streak: 16, online: true, hobbies: [{id:'dancing',name:'Танцы',level:'Профи'},{id:'running',name:'Бег',level:'Новичок'},{id:'knitting',name:'Вязание',level:'Продолжительный'}], goals: ['Освоить хобби (игра на гитаре)','Прочитать 20 книг за год','Освоить новую профессию'], bio: 'Люблю двигаться, творить и узнавать новое каждый день! 🌟', joinedMonths: 8, postsCount: 24, likesCount: 312, friendsCount: 47 },
  { id: 2, name: 'СолнышкоМое', avatar: 'https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?w=100', streak: 8, online: true, hobbies: [{id:'knitting',name:'Вязание',level:'Новичок'},{id:'drawing',name:'Рисование',level:'Любитель'}], goals: ['Создать вязаный свитер','Нарисовать портрет'], bio: 'Начинающий вязальщик, рисую кошечек 🐱', joinedMonths: 3, postsCount: 7, likesCount: 89, friendsCount: 12 },
  { id: 3, name: 'КреативКот', avatar: 'https://images.unsplash.com/photo-1599566150163-29194dcaad36?w=100', streak: 22, online: false, hobbies: [{id:'sculpting',name:'Лепка',level:'Профи'},{id:'cooking',name:'Кулинария',level:'Любитель'}], goals: ['Открыть мастер-класс','Приготовить 100 блюд'], bio: 'Профессиональный скульптор и любитель вкусно покушать 🍕', joinedMonths: 14, postsCount: 51, likesCount: 978, friendsCount: 93 },
  { id: 4, name: 'МастерЗелья', avatar: 'https://images.unsplash.com/photo-1527980965255-d3b416303d12?w=100', streak: 5, online: false, hobbies: [{id:'knitting',name:'Вязание',level:'Продолжительный'},{id:'photography',name:'Фотография',level:'Любитель'}], goals: ['Продать первое изделие','Сделать выставку фото'], bio: 'Вяжу и снимаю природу 📸', joinedMonths: 6, postsCount: 18, likesCount: 204, friendsCount: 31 },
  { id: 5, name: 'ТанцорСнов', avatar: 'https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=100', streak: 11, online: true, hobbies: [{id:'dancing',name:'Танцы',level:'Профи'},{id:'running',name:'Бег',level:'Новичок'}], goals: ['Выиграть конкурс','Пробежать марафон'], bio: 'Танцую каждый день, бегаю по утрам ☀️', joinedMonths: 10, postsCount: 33, likesCount: 567, friendsCount: 72 },
  { id: 6, name: 'ЦветокМечты', avatar: 'https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=100', streak: 3, online: false, hobbies: [{id:'sculpting',name:'Лепка',level:'Новичок'},{id:'gardening',name:'Садоводство',level:'Любитель'}], goals: ['Вырастить сад','Слепить статую'], bio: 'Сад мечты начинается с одного семечка 🌺', joinedMonths: 2, postsCount: 5, likesCount: 43, friendsCount: 8 },
];

const OTHER_USER_POSTS = {
  1: [
    { id: 101, title: 'Вязание — это медитация', text: 'Когда я вяжу, весь стресс уходит. Поделилась новым узором с подругами — все в восторге! Вот схема для тех, кто только начинает: начните с простых петель, а потом постепенно усложняйте.', img: 'https://images.unsplash.com/photo-1452860606245-08befc0ff44b?w=400', tags: ['#Вязание','#Хобби','#Советы'], likes: 54, comments: [{author:'ЗнатокОгорода',text:'Согласна, это очень расслабляет!',time:'2 ч назад'},{author:'МастерЗелья',text:'Поделись схемой!',time:'1 ч назад'}], shares: 8 },
    { id: 102, title: 'Пробежка 10 км', text: 'Сегодня побил личный рекорд! 10 км за 52 минуты. Тренировался 3 месяца, и вот наконец результат. Никогда не сдавайтесь!', img: null, tags: ['#Бег','#Спорт','#Достижение'], likes: 38, comments: [], shares: 3 },
    { id: 103, title: 'Новый танцевальный стиль', text: 'Начала изучать хастл! Первые три занятия были невероятно сложными, но сейчас уже начинаю чувствовать ритм. Очень советую всем попробовать!', img: 'https://images.unsplash.com/photo-1504609813442-a8924e83f76e?w=400', tags: ['#Танцы','#Хастл'], likes: 71, comments: [{author:'ТанцорСнов',text:'Хастл — огонь! 🔥',time:'30 мин назад'}], shares: 5 },
  ],
  2: [
    { id: 201, title: 'Первый свитер', text: 'Наконец-то связала свой первый свитер! Ушло 3 недели, но результат стоит усилий. Использовала мериносовую шерсть — мягкая и приятная.', img: 'https://images.unsplash.com/photo-1452860606245-08befc0ff44b?w=400', tags: ['#Вязание','#Новичок'], likes: 29, comments: [], shares: 2 },
    { id: 202, title: 'Мой котик в рисунке', text: 'Нарисовала своего кота акварелью! Это мой третий рисунок вообще, так что не судите строго 😊', img: null, tags: ['#Рисование','#Акварель','#Кот'], likes: 44, comments: [{author:'ПурПурПур',text:'Мило! Продолжай! 💕',time:'5 ч назад'}], shares: 1 },
  ],
  3: [
    { id: 301, title: 'Новая серия фигурок', text: 'Завершила серию из 12 миниатюрных животных из полимерной глины. Каждый занял около 3 часов. Сейчас готовлю онлайн мастер-класс!', img: null, tags: ['#Лепка','#Творчество','#МК'], likes: 91, comments: [{author:'ЦветокМечты',text:'Запишите меня на МК!',time:'3 ч назад'}], shares: 15 },
    { id: 302, title: 'Мастер-класс по лепке', text: 'Провела первый мастер-класс! 8 учеников, все довольны. Учила лепить из полимерной глины базовые фигуры.', img: 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400', tags: ['#Лепка','#МК','#Профи'], likes: 67, comments: [], shares: 9 },
  ],
};
