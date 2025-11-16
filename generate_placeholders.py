#!/usr/bin/env python3
"""Quick script to generate placeholder content for remaining topic pages"""

import os

# Template for placeholder pages
PLACEHOLDER_TEMPLATE = """{{%extends "base.html" %}}

{{%block title %}}{title} - Vidensbank{{%endblock %}}

{{%block content %}}
<header class="hero-video-container" style="background-image: url('{hero_image}');">
  <div class="bg-overlay-dark"></div>
  <div class="hero-content">
    <h1 class="hero-title">{page_title}</h1>
    <p class="hero-subtitle">{subtitle}</p>
  </div>
</header>

<section class="page-section">
  <header class="section-header">
    <p class="section-lead">{lead_text}</p>
  </header>

  <nav class="filter-nav" aria-label="Navigation" style="margin-bottom: 3rem;">
    {nav_links}
  </nav>

  <article style="max-width: 900px; margin: 0 auto;">
    <h2>{section1_title}</h2>
    <p>{section1_text}</p>

    <p style="background-color: var(--light-gron); padding: 1.5rem; border-left: 4px solid var(--dark-gron); border-radius: 4px; margin: 2rem 0;">
      <strong>For kantiner:</strong> {canteen_note}
    </p>
  </article>
</section>

<section class="section padding-y-4" style="background-color: var(--cheval-taube);">
  <div class="container" style="text-align: center;">
    <h2 class="section-title">{cta_title}</h2>
    {cta_link}
  </div>
</section>

{{%endblock %}}
"""

# Content definitions for remaining pages
PAGES_CONFIG = {
    'okologi': {
        'name': 'Økologi',
        'pages': {
            'why': {
                'title': 'Hvorfor er økologi vigtigt?',
                'subtitle': 'Miljø, dyrevelfærd og marked',
                'hero_image': 'https://images.unsplash.com/photo-1500382017468-9049fed747ef',
                'lead_text': 'Økologi har betydning for miljø, dyrevelfærd og forbrugertillid. Danmark har verdens højeste markedsandel af økologi.',
                'section1_title': 'Betydning for danske kantiner',
                'section1_text': 'Økologi er ofte en del af virksomheders bæredygtighedsmål. Mange offentlige kantiner har økologimål på 60-90%.',
                'canteen_note': 'Økologi kan styrke jeres bæredygtighedsprofil og imødekomme gæsternes forventninger.',
                'cta_title': 'Næste: Mål & Ambition',
                'next_page': 'goal'
            },
            'goal': {
                'title': 'Mål & Ambition - Økologi',
                'subtitle': 'Strategisk brug af økologi',
                'hero_image': 'https://images.unsplash.com/photo-1530836369250-ef72a3f5cda8',
                'lead_text': 'Målet er at bruge økologi strategisk som en del af en samlet bæredygtighedsstrategi.',
                'section1_title': 'Vision',
                'section1_text': 'Økologi skal være en naturlig del af kantinens sortiment uden at dominere budgettet unødigt.',
                'canteen_note': 'Kombiner økologiske valg med andre bæredygtige tiltag som lokal sourcing og plantebaseret kost.',
                'cta_title': 'Næste: Mit Aftryk',
                'next_page': 'impact'
            },
            'impact': {
                'title': 'Mit Aftryk - Økologi',
                'subtitle': 'Dine valg om økologi',
                'hero_image': 'https://images.unsplash.com/photo-1542838132-92c53300491e',
                'lead_text': 'Dit valg af økologiske råvarer påvirker både miljø, dyrevelfærd og kantinens image.',
                'section1_title': 'Strategiske valg',
                'section1_text': 'Vælg økologi hvor det giver mest mening – f.eks. mælkeprodukter, æg og grøntsager.',
                'canteen_note': 'Fokuser økologibudgettet på de varer, hvor det gør størst forskel.',
                'cta_title': 'Næste: Tips & Tricks',
                'next_page': 'tips'
            },
            'tips': {
                'title': 'Tips & Tricks - Økologi',
                'subtitle': 'Praktisk brug af økologi',
                'hero_image': 'https://images.unsplash.com/photo-1518843875459-f738682238a6',
                'lead_text': 'Konkrete metoder til at øge økologiandelen uden at sprænge budgettet.',
                'section1_title': 'Budgetvenlige strategier',
                'section1_text': 'Brug økologi på basisvarer som mælk, æg, pasta og ris. Kombiner med sæsonvarer og lokale leverandører.',
                'canteen_note': 'Planlæg menuen efter, hvilke økologiske råvarer der er tilgængelige og prisvenlige.',
                'cta_title': 'Tilbage til emnet',
                'next_page': 'landing'
            }
        }
    },
    'vandforbrug': {
        'name': 'Vandforbrug',
        'pages': {
            'what': {
                'title': 'Hvad er vandforbrug i fødevareproduktion?',
                'subtitle': 'Blåt, grønt og gråt vand',
                'hero_image': 'https://images.unsplash.com/photo-1578575437130-527eed3abbec',
                'lead_text': 'Vandaftryk måler hvor meget vand der bruges til at producere fødevarer. Det omfatter både direkte vanding og vand i forsyningskæden.',
                'section1_title': 'De tre typer vand',
                'section1_text': 'Blåt vand er overfladevand, grønt vand er regnvand, og gråt vand er forurenet vand der skal renses.',
                'canteen_note': 'Nogle fødevarer kræver enormt meget vand – f.eks. kød og nødder.',
                'cta_title': 'Næste: Hvorfor er det vigtigt?',
                'next_page': 'why'
            },
            'why': {
                'title': 'Hvorfor er vandforbrug vigtigt?',
                'subtitle': 'Vandknaphed globalt',
                'hero_image': 'https://images.unsplash.com/photo-1559827260-dc66d52bef19',
                'lead_text': 'Globalt er ferskvand en knap ressource. Fødevareproduktion står for omkring 70% af det globale vandforbrug.',
                'section1_title': 'Betydning for Danmark',
                'section1_text': 'Selvom Danmark har rigeligt vand, importerer vi fødevarer fra vandknappe områder.',
                'canteen_note': 'Ved at vælge råvarer med lavere vandaftryk kan kantiner bidrage til global vandsikkerhed.',
                'cta_title': 'Næste: Mål & Ambition',
                'next_page': 'goal'
            },
            'goal': {
                'title': 'Mål & Ambition - Vandforbrug',
                'subtitle': 'Vandbevidste valg',
                'hero_image': 'https://images.unsplash.com/photo-1559825481-12a05cc00344',
                'lead_text': 'Målet er at integrere vandbevidsthed i indkøbsbeslutninger.',
                'section1_title': 'Vision',
                'section1_text': 'Kantiner skal kunne vælge råvarer med lavere vandaftryk hvor det er relevant.',
                'canteen_note': 'Kombiner vandbevidsthed med klimahensyn for en helhedsorienteret tilgang.',
                'cta_title': 'Næste: Mit Aftryk',
                'next_page': 'impact'
            },
            'impact': {
                'title': 'Mit Aftryk - Vandforbrug',
                'subtitle': 'Råvarevalg og vand',
                'hero_image': 'https://images.unsplash.com/photo-1523301343968-6a6ebf63c672',
                'lead_text': 'Dit valg af protein og grøntsager påvirker indirekte vandforbruget.',
                'section1_title': 'Vand-intensive fødevarer',
                'section1_text': 'Oksekød, lam, nødder og ris har højt vandforbrug. Kylling, bælgfrugter og de fleste grøntsager har lavere aftryk.',
                'canteen_note': 'Små justeringer i menusammensætning kan reducere vandaftrykket betydeligt.',
                'cta_title': 'Næste: Tips & Tricks',
                'next_page': 'tips'
            },
            'tips': {
                'title': 'Tips & Tricks - Vandforbrug',
                'subtitle': 'Praktiske greb',
                'hero_image': 'https://images.unsplash.com/photo-1551836022-aadb801c60ae',
                'lead_text': 'Konkrete metoder til at reducere vandaftryk gennem menuvalg.',
                'section1_title': 'Strategier',
                'section1_text': 'Prioriter kylling over oksekød, bælgfrugter over nødder, og europæiske grøntsager over importvarer fra tørre områder.',
                'canteen_note': 'Data om vandaftryk kan kombineres med klimadata for bedre beslutningsgrundlag.',
                'cta_title': 'Tilbage til emnet',
                'next_page': 'landing'
            }
        }
    },
    'madspild': {
        'name': 'Madspild',
        'pages': {
            'what': {
                'title': 'Hvad er madspild?',
                'subtitle': 'Definition og omfang',
                'hero_image': 'https://images.unsplash.com/photo-1466637574441-749b8f19452f',
                'lead_text': 'Madspild er mad, der kunne have været spist af mennesker, men som i stedet smides væk eller går til andet formål.',
                'section1_title': 'De tre typer madspild',
                'section1_text': 'Produktionsspild (i køkkenet), buffetspild (overskud) og tallerkenssp ild (fra gæster).',
                'canteen_note': 'Danske kantiner smider i gennemsnit 20-30% af maden væk – et enormt potentiale for forbedring.',
                'cta_title': 'Næste: Hvorfor er det vigtigt?',
                'next_page': 'why'
            },
            'why': {
                'title': 'Hvorfor er madspild vigtigt?',
                'subtitle': 'Klima, økonomi og etik',
                'hero_image': 'https://images.unsplash.com/photo-1532996122724-e3c354a0b15b',
                'lead_text': 'Madspild er et af de største klimaproblemer i fødevaresystemet, og koster samtidig kantiner mange penge.',
                'section1_title': 'Det tredobbelte tab',
                'section1_text': 'Madspild betyder spildt klima, spildte penge og spildte ressourcer.',
                'canteen_note': 'Reduktion af madspild er ofte det mest omkostningseffektive bæredygtighedstiltag en kantine kan lave.',
                'cta_title': 'Næste: Mål & Ambition',
                'next_page': 'goal'
            },
            'goal': {
                'title': 'Mål & Ambition - Madspild',
                'subtitle': 'Halvering af spild',
                'hero_image': 'https://images.unsplash.com/photo-1542838132-92c53300491e',
                'lead_text': 'Målet er at halvere madspildet fra nuværende niveau gennem systematisk måling og handling.',
                'section1_title': 'Vision',
                'section1_text': 'Kantiner skal kunne måle, forstå og reducere madspild på tværs af alle faser.',
                'canteen_note': 'Start med at måle i en periode for at finde de største spildkilder.',
                'cta_title': 'Næste: Mit Aftryk',
                'next_page': 'impact'
            },
            'impact': {
                'title': 'Mit Aftryk - Madspild',
                'subtitle': 'Din rolle',
                'hero_image': 'https://images.unsplash.com/photo-1588964895597-cfccd6e2dbf9',
                'lead_text': 'Dit ansvar for portionering, produktion og kommunikation påvirker direkte madspildet.',
                'section1_title': 'Hvor du kan gøre en forskel',
                'section1_text': 'Planlæg produktionen bedre, optimer portionsstørrelser, og gør det nemt for gæster at tage mindre.',
                'canteen_note': 'De fleste kantiner kan reducere spild med 30-50% gennem bedre planlægning alene.',
                'cta_title': 'Næste: Tips & Tricks',
                'next_page': 'tips'
            },
            'tips': {
                'title': 'Tips & Tricks - Madspild',
                'subtitle': 'Praktiske værktøjer',
                'hero_image': 'https://images.unsplash.com/photo-1504674900247-0877df9cc836',
                'lead_text': 'Konkrete metoder til at måle, forstå og reducere madspild i kantinen.',
                'section1_title': 'Kom i gang',
                'section1_text': 'Mål spild i en uge, identificer de største kilder, og sæt mål for reduktion. Brug historiske data til bedre planlægning.',
                'canteen_note': 'Små justeringer kan have stor effekt – start et sted og byg videre.',
                'cta_title': 'Tilbage til emnet',
                'next_page': 'landing'
            }
        }
    }
}

def create_nav_links(topic, current_page, next_page):
    """Generate navigation links"""
    links = []
    if current_page == 'what':
        links.append(f'<a href="{{{{{{ url_for(\'topic_{topic}_landing\') }}}}}}" class="filter-pill">← Tilbage til emnet</a>')
    else:
        prev_pages = {'why': 'what', 'goal': 'why', 'impact': 'goal', 'tips': 'impact'}
        if current_page in prev_pages:
            links.append(f'<a href="{{{{{{ url_for(\'topic_{topic}_{prev_pages[current_page]}\') }}}}}}" class="filter-pill">← Forrige</a>')
        links.append(f'<a href="{{{{{{ url_for(\'topic_{topic}_landing\') }}}}}}" class="filter-pill">Tilbage til emnet</a>')

    if next_page and next_page != 'landing':
        links.append(f'<a href="{{{{{{ url_for(\'topic_{topic}_{next_page}\') }}}}}}" class="filter-pill">Næste →</a>')

    return '\n    '.join(links)

def create_cta_link(topic, next_page):
    """Generate CTA link"""
    if next_page == 'landing':
        return f'<a href="{{{{{{ url_for(\'topic_{topic}_landing\') }}}}}}" class="btn-primary" style="margin-top: 1.5rem;">Tilbage til emnet</a>'
    return f'<a href="{{{{{{ url_for(\'topic_{topic}_{next_page}\') }}}}}}" class="btn-primary" style="margin-top: 1.5rem;">Læs mere →</a>'

def generate_pages():
    """Generate all placeholder pages"""
    base_dir = 'templates/topics'

    for topic, config in PAGES_CONFIG.items():
        for page_type, content in config['pages'].items():
            # Create page content
            page_content = PLACEHOLDER_TEMPLATE.format(
                title=content['title'],
                page_title=content['title'],
                subtitle=content['subtitle'],
                hero_image=content['hero_image'],
                lead_text=content['lead_text'],
                nav_links=create_nav_links(topic, page_type, content['next_page']),
                section1_title=content['section1_title'],
                section1_text=content['section1_text'],
                canteen_note=content['canteen_note'],
                cta_title=content['cta_title'],
                cta_link=create_cta_link(topic, content['next_page'])
            )

            # Write file
            file_path = os.path.join(base_dir, topic, f'{page_type}.html')
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(page_content)

            print(f'Created: {file_path}')

if __name__ == '__main__':
    generate_pages()
    print('\n✅ All placeholder pages generated successfully!')
