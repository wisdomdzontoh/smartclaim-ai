// app/page.tsx
import Link from 'next/link'

export default function LandingPage() {
  return (
    <main className="bg-gray-50 text-gray-800">
      {/* Hero */}
      <section className="pt-20 pb-12">
        <div className="container mx-auto px-6 md:px-12 flex flex-col-reverse lg:flex-row items-center">
          {/* Text */}
          <div className="w-full lg:w-1/2 text-center lg:text-left">
            <h1 className="text-5xl md:text-6xl font-extrabold leading-tight mb-4">
              Transform Insurance Claims with AI
            </h1>
            <p className="text-lg md:text-xl text-gray-600 mb-6 max-w-xl mx-auto lg:mx-0">
              SmartClaim AI automates claim intake, speeds up review, flags fraud
              and keeps your data strictly separated by tenant—all in one platform.
            </p>
            <div className="flex flex-col sm:flex-row sm:justify-center lg:justify-start gap-4">
              <Link
                href="/company-signup"
                className="px-6 py-3 bg-blue-600 text-white font-medium rounded-md hover:bg-blue-700 transition"
              >
                I’m an Insurer
              </Link>
              <Link
                href="/register"
                className="px-6 py-3 border-2 border-blue-600 text-blue-600 font-medium rounded-md hover:bg-blue-50 transition"
              >
                I’m a Customer
              </Link>
            </div>
          </div>

          {/* Illustration */}
          <div className="w-full lg:w-1/2 mb-10 lg:mb-0">
            <img
              src="/hero-illustration.svg"
              alt="Dashboard illustration"
              className="w-full h-auto mx-auto"
            />
          </div>
        </div>
      </section>

      {/* Features */}
      <section className="py-16">
        <div className="container mx-auto px-6 md:px-12 text-center">
          <h2 className="text-3xl md:text-4xl font-bold mb-10">
            Why SmartClaim AI?
          </h2>
          <div className="grid gap-8 grid-cols-1 sm:grid-cols-2 lg:grid-cols-3">
            <div className="p-6 bg-white rounded-lg shadow-sm">
              <h3 className="text-xl font-semibold mb-2">AI Summarization</h3>
              <p className="text-gray-600">
                Instantly distill long-form claim descriptions into concise
                summaries for faster decision-making.
              </p>
            </div>
            <div className="p-6 bg-white rounded-lg shadow-sm">
              <h3 className="text-xl font-semibold mb-2">Fraud Detection</h3>
              <p className="text-gray-600">
                Leverage machine learning to flag suspicious claims before they
                cost you millions.
              </p>
            </div>
            <div className="p-6 bg-white rounded-lg shadow-sm">
              <h3 className="text-xl font-semibold mb-2">Multi-Tenant Security</h3>
              <p className="text-gray-600">
                Each insurer’s data is siloed and encrypted, with role-based
                access control.
              </p>
            </div>
            <div className="p-6 bg-white rounded-lg shadow-sm">
              <h3 className="text-xl font-semibold mb-2">Automatic Routing</h3>
              <p className="text-gray-600">
                Assign claims to handlers or supervisors based on priority,
                workload, or custom rules.
              </p>
            </div>
            <div className="p-6 bg-white rounded-lg shadow-sm">
              <h3 className="text-xl font-semibold mb-2">Real-Time Dashboard</h3>
              <p className="text-gray-600">
                Monitor incoming claims, processing stages, and SLA metrics at
                a glance.
              </p>
            </div>
            <div className="p-6 bg-white rounded-lg shadow-sm">
              <h3 className="text-xl font-semibold mb-2">Scalable & Extensible</h3>
              <p className="text-gray-600">
                Built on Django, DRF, Celery and Next.js for easy customization
                and horizontal scaling.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-800 text-gray-400 py-8">
        <div className="container mx-auto px-6 md:px-12 text-center">
          <p className="mb-4">&copy; {new Date().getFullYear()} SmartClaim AI. All rights reserved.</p>
          <div className="space-x-4">
            <Link href="/privacy" className="hover:text-white">
              Privacy Policy
            </Link>
            <Link href="/terms" className="hover:text-white">
              Terms of Service
            </Link>
            <Link href="/contact" className="hover:text-white">
              Contact Us
            </Link>
          </div>
        </div>
      </footer>
    </main>
)
}
