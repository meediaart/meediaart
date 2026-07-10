from app import create_app
from app.extensions import db
from app.models.service import Service
from app.models.post import Post
from app.models.project import Project
from app.models.category import Category
from app.models.product import Product
from app.models.menu_item import MenuItem
from app.models.menu_item import MenuItem


app = create_app()

with app.app_context():
    menu_items = [
    MenuItem(title="الرئيسية", endpoint="main.home", position=1),
    MenuItem(title="من نحن", endpoint="about.index", position=2),
    MenuItem(title="الخدمات", endpoint="services.index", position=3),
    MenuItem(title="معرض الأعمال", endpoint="portfolio.index", position=4),
    MenuItem(title="المتجر", endpoint="shop.index", position=5),
    MenuItem(title="المدونة", endpoint="blog.index", position=6),
    MenuItem(title="تواصل معنا", endpoint="contact.index", position=7),
]

    db.session.add_all(menu_items)
    db.session.commit()
    # الخدمات
    if Service.query.count() == 0:
        services = [
            Service(
                title="تصميم المواقع",
                slug="web-design",
                keywords="تصميم مواقع",
                description="نقدم خدمات تصميم مواقع احترافية ومتجاوبة مع جميع الأجهزة."
            ),
            Service(
                title="الأمن السيبراني",
                slug="cybersecurity",
                keywords="أمن سيبراني",
                description="نوفر حلولًا للحماية، التقييم الأمني، وتعزيز أمن البنية الرقمية."
            ),
            Service(
                title="التسويق الرقمي",
                slug="digital-marketing",
                keywords="تسويق رقمي",
                description="نساعدك على الوصول إلى جمهورك عبر استراتيجيات تسويق رقمية فعالة."
            ),
        ]
        db.session.add_all(services)

    # المقالات
    if Post.query.count() == 0:
        posts = [
            Post(
                title="أهمية تصميم المواقع الحديثة",
                slug="modern-web-design",
                content="تصميم المواقع الحديثة يساعد على تحسين تجربة المستخدم وزيادة التحويل."
            ),
            Post(
                title="أساسيات الأمن السيبراني للشركات",
                slug="cybersecurity-basics",
                content="الأمن السيبراني ضروري لحماية البيانات والأنظمة من التهديدات."
            ),
            Post(
                title="كيف تنجح في التسويق الرقمي",
                slug="digital-marketing-success",
                content="النجاح في التسويق الرقمي يعتمد على الاستراتيجية والتحليل المستمر."
            ),
        ]
        db.session.add_all(posts)

    # المشاريع
    if Project.query.count() == 0:
        projects = [
            Project(
                title="موقع شركة تقنية",
                slug="tech-company-website",
                description="مشروع تصميم وتطوير موقع احترافي لشركة تقنية."
            ),
            Project(
                title="متجر ميداليات",
                slug="medals-store",
                description="مشروع متجر إلكتروني لبيع الميداليات والمنتجات المخصصة."
            ),
            Project(
                title="هوية بصرية لمؤسسة",
                slug="brand-identity",
                description="تصميم هوية بصرية متكاملة لمؤسسة تجارية."
            ),
        ]
        db.session.add_all(projects)

    # التصنيفات
    medals_category = Category.query.filter_by(slug="medals").first()
    if not medals_category:
        medals_category = Category(name="ميداليات", slug="medals")
        db.session.add(medals_category)

    models_category = Category.query.filter_by(slug="models").first()
    if not models_category:
        models_category = Category(name="مجسمات", slug="models")
        db.session.add(models_category)

    decor_category = Category.query.filter_by(slug="decor").first()
    if not decor_category:
        decor_category = Category(name="ديكورات", slug="decor")
        db.session.add(decor_category)

    # القائمة الرئيسية
    if MenuItem.query.count() == 0:
        menu_items = [
            MenuItem(title="الرئيسية", endpoint="main.home", display_order=1, is_active=True),
            MenuItem(title="من نحن", endpoint="about.index", display_order=2, is_active=True),
            MenuItem(title="الخدمات", endpoint="services.index", display_order=3, is_active=True),
            MenuItem(title="معرض الأعمال", endpoint="portfolio.index", display_order=4, is_active=True),
            MenuItem(title="المتجر", endpoint="shop.index", display_order=5, is_active=True),
            MenuItem(title="المدونة", endpoint="blog.index", display_order=6, is_active=True),
            MenuItem(title="تواصل معنا", endpoint="contact.index", display_order=7, is_active=True),
        ]
        db.session.add_all(menu_items)

    db.session.commit()

    # المنتجات
    if Product.query.count() == 0:
        products = [
            Product(
                title="ميدالية ذهبية",
                slug="gold-medal",
                description="ميدالية بتصميم أنيق ومخصصة للمناسبات والفعاليات.",
                price=99.99,
                category_id=medals_category.id
            ),
            Product(
                title="ميدالية فضية",
                slug="silver-medal",
                description="ميدالية فضية عالية الجودة.",
                price=79.99,
                category_id=medals_category.id
            ),
            Product(
                title="مجسم برج",
                slug="tower-model",
                description="مجسم ديكوري مناسب للمكاتب والمنازل.",
                price=149.99,
                category_id=models_category.id
            ),
            Product(
                title="مجسم سيارة",
                slug="car-model",
                description="مجسم سيارة بتفاصيل جميلة.",
                price=129.99,
                category_id=models_category.id
            ),
            Product(
                title="ديكور حائط",
                slug="wall-decor",
                description="قطعة ديكور أنيقة لتزيين الحائط.",
                price=89.99,
                category_id=decor_category.id
            ),
            Product(
                title="قطعة مكتبية",
                slug="desk-piece",
                description="قطعة مكتبية ديكورية وعملية.",
                price=59.99,
                category_id=decor_category.id
            ),
        ]
        db.session.add_all(products)
        

    db.session.commit()
    print("✅ تم تجهيز البيانات وربط المنتجات بالتصنيفات والقائمة الرئيسية بنجاح")