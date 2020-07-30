from django.db import models
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import reverse
from django.db.models.signals import post_delete
from django.dispatch import receiver

# Create your models here.

def get_image_filename(instance, filename):
    title = instance
    slug = slugify(title)
    folder_name = instance.__class__.__name__.lower()
    return "%s/%s-%s" % (folder_name, slug, filename)  

def unique_slug_generator(instance, text, new_slug=None):
    slug = slugify(text)
    new_slug = slug
    Klass = instance.__class__
    numb = 1
    while Klass.objects.filter(slug=new_slug).exists():
        new_slug = "{slug}-{num}".format(
            slug=slug,
            num=numb
        )
        numb += 1
    return new_slug


class BaseModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True, verbose_name=_('Creation Date'))
    modified_date = models.DateTimeField(auto_now=True , verbose_name=_('Modified Date'))

    class Meta:
        abstract = True


class Categories(BaseModel):
    category_name = models.CharField(max_length=50, unique=True)
    category_image = models.ImageField(upload_to = get_image_filename)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')

    def save(self, *args, **kwargs):
        self.slug = unique_slug_generator(self ,self.category_name)
        super(Categories, self).save(*args, **kwargs)

    def __str__(self):
        return self.category_name
        

    def get_absolute_url(self):
        return reverse("product:category", kwargs={
            'slug': self.slug
        })


class Products(BaseModel):
    category = models.ForeignKey(Categories, related_name="products", 
                                default=None, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=100, verbose_name=_('Product Name'))
    product_price = models.FloatField(verbose_name=_('Product Price'))
    description = models.TextField()
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = _('product')
        verbose_name_plural = _('products')

    def save(self, *args, **kwargs):
        self.slug = unique_slug_generator(self ,self.product_name)
        super(Products, self).save(*args, **kwargs)

    def __str__(self):
        return self.product_name

    def get_absolute_url(self):
        return reverse("product:product", kwargs={
            'slug': self.slug
        })


class ProductImages(BaseModel):
    product = models.ForeignKey(Products, related_name="product_images",
                                default=None, on_delete=models.CASCADE)
    image = models.ImageField(upload_to = get_image_filename,
                              verbose_name='Image')
    
    class Meta:
        verbose_name = _('Product Image')
        verbose_name_plural = _('Product Images')


class ProductFeatures(BaseModel):
    product = models.ForeignKey(Products, related_name="product_features",
                                default=None, on_delete=models.CASCADE)
    feature = models.TextField()

    class Meta:
        verbose_name = _('Product Feature')
        verbose_name_plural = _('Product Features')

    def __str__(self):
        return self.feature


@receiver(post_delete, sender=Categories)
def category_image_delete(sender, instance, **kwargs):
    instance.category_image.delete(False) 

@receiver(post_delete, sender=ProductImages)
def product_image_delete(sender, instance, **kwargs):
    instance.image.delete(False) 