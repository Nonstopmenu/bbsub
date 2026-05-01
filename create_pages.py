import os

base_path = '/home/barboss/Рабочий стол/BB.sub/public/'
with open(os.path.join(base_path, 'index.html'), 'r', encoding='utf-8') as f:
    lines = f.readlines()

header_end = 0
for i, line in enumerate(lines):
    if '<!-- Mega Menu -->' in line:
        pass # Mega menu starts here
    if '<section class="hero">' in line:
        header_end = i
        break

footer_start = 0
for i, line in enumerate(lines):
    if '<footer>' in line:
        footer_start = i
        break

header_content = ''.join(lines[:header_end])
# We need to change the mega menu links in the header content to use actual links instead of #
header_content = header_content.replace('href="#">Блог', 'href="/blog">Блог')
header_content = header_content.replace('href="#">История бренда', 'href="/history">История бренда')
header_content = header_content.replace('href="#">Правила подписки', 'href="/rules">Правила подписки')
header_content = header_content.replace('href="#">Политика конфиденциальности', 'href="/privacy">Политика конфиденциальности')
header_content = header_content.replace('href="#">Контакты', 'href="/contacts">Контакты')

footer_content = ''.join(lines[footer_start:])
footer_content = footer_content.replace('href="#">Оферта', 'href="/terms">Оферта')
footer_content = footer_content.replace('href="#">Политика конфиденциальности', 'href="/privacy">Политика конфиденциальности')
footer_content = footer_content.replace('href="#">Instagram', 'href="https://instagram.com" target="_blank">Instagram')


pages = {
    'terms': 'Публичная оферта',
    'privacy': 'Политика конфиденциальности',
    'blog': 'Наш Блог',
    'history': 'История бренда Bb.sub',
    'rules': 'Правила подписки',
    'contacts': 'Контакты'
}

content_map = {
    'terms': """
        <p style="margin-bottom: 1.5rem; color: var(--text-muted); line-height: 1.8;">
            Настоящая Публичная оферта является официальным предложением сервиса Bb.sub на заключение договора абонентского обслуживания (подписки на бьюти-боксы).
        </p>
        <h3 style="margin: 2rem 0 1rem 0; color: var(--dark); font-size: 1.5rem;">1. Предмет договора</h3>
        <p style="margin-bottom: 1.5rem; color: var(--text-muted); line-height: 1.8;">
            1.1. Сервис обязуется на регулярной основе (ежемесячно) формировать и доставлять Пользователю бьюти-бокс, состав которого определяется алгоритмом на основе заполненной анкеты.
            <br>1.2. Пользователь обязуется своевременно оплачивать стоимость выбранного тарифа.
        </p>
        <h3 style="margin: 2rem 0 1rem 0; color: var(--dark); font-size: 1.5rem;">2. Оплата и доставка</h3>
        <p style="margin-bottom: 1.5rem; color: var(--text-muted); line-height: 1.8;">
            Списание средств происходит автоматически каждый месяц в дату первоначального оформления. Доставка осуществляется курьерской службой в течение 3-5 рабочих дней после сборки.
        </p>
    """,
    'privacy': """
        <p style="margin-bottom: 1.5rem; color: var(--text-muted); line-height: 1.8;">
            Мы в Bb.sub невероятно серьезно относимся к вашей приватности. Данная политика описывает, как мы собираем, храним и используем ваши данные.
        </p>
        <h3 style="margin: 2rem 0 1rem 0; color: var(--dark); font-size: 1.5rem;">Сбор данных</h3>
        <p style="margin-bottom: 1.5rem; color: var(--text-muted); line-height: 1.8;">
            Мы собираем информацию о типе вашей кожи, предпочтениях и бюджете исключительно для того, чтобы алгоритм мог подобрать идеальные продукты для вашего бокса. Мы никогда не передаем эти данные третьим лицам.
        </p>
        <h3 style="margin: 2rem 0 1rem 0; color: var(--dark); font-size: 1.5rem;">Безопасность платежей</h3>
        <p style="margin-bottom: 1.5rem; color: var(--text-muted); line-height: 1.8;">
            Все транзакции защищены протоколом шифрования банковского уровня. Мы не храним полные данные ваших кредитных карт на своих серверах.
        </p>
    """,
    'blog': """
        <div style="display: grid; grid-template-columns: 1fr; gap: 2rem;">
            <div style="border-bottom: 1px solid rgba(0,0,0,0.1); padding-bottom: 2rem;">
                <div style="color: var(--primary); font-size: 0.9rem; margin-bottom: 0.5rem; font-weight: bold;">ТРЕНДЫ</div>
                <h2 style="font-size: 1.8rem; margin-bottom: 1rem; color: var(--dark);">Минимализм в уходе: почему меньше значит лучше?</h2>
                <p style="color: var(--text-muted); line-height: 1.6; margin-bottom: 1rem;">В 2026 году многоступенчатый корейский уход окончательно уступил место skin-minimalism. Разбираем, почему нашей коже нужен отдых и какие 3 продукта заменят целую полку...</p>
                <a href="#" style="color: var(--primary); font-weight: 500;">Читать далее →</a>
            </div>
            <div style="border-bottom: 1px solid rgba(0,0,0,0.1); padding-bottom: 2rem;">
                <div style="color: var(--primary); font-size: 0.9rem; margin-bottom: 0.5rem; font-weight: bold;">ИНГРЕДИЕНТЫ</div>
                <h2 style="font-size: 1.8rem; margin-bottom: 1rem; color: var(--dark);">Вся правда о ретиноле: как начать и не навредить</h2>
                <p style="color: var(--text-muted); line-height: 1.6; margin-bottom: 1rem;">Ретинол остается золотым стандартом anti-age ухода, но многие боятся его побочных эффектов. В этой статье мы собрали советы лучших дерматологов...</p>
                <a href="#" style="color: var(--primary); font-weight: 500;">Читать далее →</a>
            </div>
        </div>
    """,
    'history': """
        <p style="margin-bottom: 1.5rem; color: var(--text-muted); line-height: 1.8; font-size: 1.1rem;">
            История Bb.sub началась не в сверкающих лабораториях крупных корпораций, а в темных коридорах университетского кампуса.
        </p>
        <p style="margin-bottom: 1.5rem; color: var(--text-muted); line-height: 1.8;">
            Группа крайне скрытных студентов факультета биохимии была одержима составами косметических средств. Они часами анализировали формулы люксовых кремов и понимали, что маркетинг часто забирает 90% бюджета, оставляя на активные ингредиенты копейки.
        </p>
        <div style="padding: 2rem; background: var(--secondary); border-radius: 12px; margin: 2rem 0;">
            <p style="font-style: italic; color: var(--dark); font-size: 1.2rem; text-align: center; margin: 0;">
                "Мы хотели взломать индустрию красоты, сделав люксовый, работающий уход доступным по подписке".
            </p>
        </div>
        <p style="margin-bottom: 1.5rem; color: var(--text-muted); line-height: 1.8;">
            Сначала они собирали кастомные наборы ингредиентов (бьюти-боксы) только для "своих" — закрытого сообщества. Когда слухи о чудо-боксах вышли за пределы университета, основатели поняли, что им нужна технологичная платформа. Так родился алгоритм персонализации и сервис Bb.sub. До сих пор основатели проекта предпочитают оставаться в тени, позволяя качеству продуктов говорить за себя.
        </p>
    """,
    'rules': """
        <ol style="margin-bottom: 1.5rem; color: var(--text-muted); line-height: 1.8; padding-left: 1.5rem; font-size: 1.1rem;">
            <li style="margin-bottom: 1rem;"><strong style="color: var(--dark);">Пройдите тест:</strong> Заполните короткую анкету о вашей коже и предпочтениях. Алгоритм обработает данные.</li>
            <li style="margin-bottom: 1rem;"><strong style="color: var(--dark);">Выберите тариф:</strong> Economy, Premium или Lux. Разница лишь в количестве и классе брендов, персонализация работает идеально на всех тарифах.</li>
            <li style="margin-bottom: 1rem;"><strong style="color: var(--dark);">Ежемесячная магия:</strong> Каждый месяц мы собираем для вас уникальную коробку с полноразмерными продуктами.</li>
            <li style="margin-bottom: 1rem;"><strong style="color: var(--dark);">Полная свобода:</strong> Вы можете поставить подписку на паузу, пропустить месяц или отменить её в любой момент в Личном кабинете без штрафов и скрытых комиссий.</li>
        </ol>
    """
}

for slug, title in pages.items():
    page_content = f"""
    <section class="page-content" style="padding-top: 150px; min-height: 70vh;">
        <div class="container" style="max-width: 800px; margin: 0 auto;">
            <h1 style="font-size: 3rem; margin-bottom: 2rem; color: var(--dark); font-family: 'Outfit', sans-serif;">{title}</h1>
            <div class="text-content">
                {content_map.get(slug, '') if slug != 'contacts' else '''
                <p style="font-size: 1.2rem; margin-bottom: 2rem;">Свяжитесь с нами по любым вопросам. Мы всегда рады помочь!</p>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 2rem; margin-top: 3rem;">
                    <div style="background: var(--light); padding: 2rem; border-radius: 12px;">
                        <h4 style="margin-bottom: 1rem;">Email</h4>
                        <a href="mailto:hello@bbsub.kz" style="color: var(--primary); font-size: 1.2rem;">hello@bbsub.kz</a>
                    </div>
                    <div style="background: var(--light); padding: 2rem; border-radius: 12px;">
                        <h4 style="margin-bottom: 1rem;">Социальные сети</h4>
                        <a href="#" style="color: var(--primary); font-size: 1.2rem; display: block; margin-bottom: 0.5rem;">Instagram</a>
                        <a href="#" style="color: var(--primary); font-size: 1.2rem; display: block;">Telegram</a>
                    </div>
                </div>
                '''}
            </div>
        </div>
    </section>
    """
    
    with open(os.path.join(base_path, f'{slug}.html'), 'w', encoding='utf-8') as f:
        # We need to change the title for each page slightly
        page_header = header_content.replace('<title>Bb.sub — Идеальный уход, подобранный именно для тебя</title>', f'<title>{title} — Bb.sub</title>')
        f.write(page_header + page_content + footer_content)

# Update index.html mega menu and footer links
with open(os.path.join(base_path, 'index.html'), 'w', encoding='utf-8') as f:
    f.write(header_content + ''.join(lines[header_end:footer_start]) + footer_content)

print("Created 6 pages and updated index.html")
