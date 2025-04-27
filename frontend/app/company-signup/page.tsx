// app/company-signup/page.tsx
'use client'

import { useState, FormEvent } from 'react'
import { useRouter } from 'next/navigation'
import API from '@/lib/api'
import { Input } from '@/components/ui/input'
import { Button } from '@/components/ui/button'

type FormState = {
  // Step 1: company
  name: string
  website: string
  contactEmail: string
  contactPhone: string
  address: string
  industry: string
  timezone: string
  defaultLanguage: string
  subscriptionPlan: string
  // Step 2: admin
  adminUsername: string
  adminEmail: string
  adminPassword: string
  adminPassword2: string
}

export default function CompanySignupPage() {
  const router = useRouter()
  const [step, setStep] = useState<1 | 2>(1)
  const [form, setForm] = useState<FormState>({
    name: '',
    website: '',
    contactEmail: '',
    contactPhone: '',
    address: '',
    industry: '',
    timezone: 'UTC',
    defaultLanguage: 'en',
    subscriptionPlan: 'free',
    adminUsername: '',
    adminEmail: '',
    adminPassword: '',
    adminPassword2: '',
  })
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)

  const industryOptions = [
    'Insurance', 'Manufacturing', 'Retail', 'Other'
  ]
  const languageOptions = ['en','de','fr']
  const timezoneOptions = [
    'UTC',
    'Europe/London',
    'Europe/Berlin',
    'America/New_York',
    'Asia/Tokyo'
  ]
  const planOptions = [
    'free','basic','premium','enterprise'
  ]

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>
  ) => {
    const { name, value } = e.target
    setForm(f => ({ ...f, [name]: value }))
  }

  const canProceedToStep2 = () =>
    form.name.trim() !== '' &&
    form.contactEmail.trim() !== ''

  const handleNext = () => {
    if (!canProceedToStep2()) {
      setError('Company name and contact email are required.')
      return
    }
    setError(null)
    setStep(2)
  }

  const handleBack = () => {
    setError(null)
    setStep(1)
  }

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault()
    if (form.adminPassword !== form.adminPassword2) {
      setError("Passwords don't match")
      return
    }
    setLoading(true)
    setError(null)

    try {
      const { data } = await API.post('companies/register/', {
        name:             form.name,
        website:          form.website,
        contact_email:    form.contactEmail,
        contact_phone:    form.contactPhone,
        address:          form.address,
        industry:         form.industry,
        timezone:         form.timezone,
        default_language: form.defaultLanguage,
        subscription_plan:form.subscriptionPlan,
        admin_username:   form.adminUsername,
        admin_email:      form.adminEmail,
        admin_password:   form.adminPassword,
      })
      localStorage.setItem('access_token', data.access)
      localStorage.setItem('refresh_token', data.refresh)
      router.push('/dashboard')
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Registration failed')
      setLoading(false)
    }
  }

  return (
    <main className="max-w-lg mx-auto py-10 px-4">
      <h1 className="text-2xl font-bold mb-6">
        {step === 1 ? 'Step 1: Company Details' : 'Step 2: Admin Account'}
      </h1>
      {error && (
        <div className="mb-4 p-2 bg-red-100 text-red-700 rounded">
          {error}
        </div>
      )}
      <form onSubmit={handleSubmit} className="space-y-4">
        {step === 1 && (
          <>
            <Input
              name="name"
              placeholder="Company Name"
              value={form.name}
              onChange={handleChange}
              required
            />
            <Input
              name="website"
              placeholder="Website (https://...)"
              value={form.website}
              onChange={handleChange}
            />
            <Input
              name="contactEmail"
              type="email"
              placeholder="Contact Email"
              value={form.contactEmail}
              onChange={handleChange}
              required
            />
            <Input
              name="contactPhone"
              placeholder="Contact Phone"
              value={form.contactPhone}
              onChange={handleChange}
            />
            <Input
              name="address"
              placeholder="Address"
              value={form.address}
              onChange={handleChange}
            />
            <div>
              <label className="block mb-1 font-medium">Industry</label>
              <select
                name="industry"
                value={form.industry}
                onChange={handleChange}
                className="w-full px-3 py-2 border rounded"
              >
                <option value="">Select Industry</option>
                {industryOptions.map(i => (
                  <option key={i} value={i}>{i}</option>
                ))}
              </select>
            </div>
            <div>
              <label className="block mb-1 font-medium">Timezone</label>
              <select
                name="timezone"
                value={form.timezone}
                onChange={handleChange}
                className="w-full px-3 py-2 border rounded"
              >
                {timezoneOptions.map(tz => (
                  <option key={tz} value={tz}>{tz}</option>
                ))}
              </select>
            </div>
            <div>
              <label className="block mb-1 font-medium">Default Language</label>
              <select
                name="defaultLanguage"
                value={form.defaultLanguage}
                onChange={handleChange}
                className="w-full px-3 py-2 border rounded"
              >
                {languageOptions.map(lang => (
                  <option key={lang} value={lang}>{lang.toUpperCase()}</option>
                ))}
              </select>
            </div>
            <div>
              <label className="block mb-1 font-medium">Subscription Plan</label>
              <select
                name="subscriptionPlan"
                value={form.subscriptionPlan}
                onChange={handleChange}
                className="w-full px-3 py-2 border rounded"
              >
                {planOptions.map(p => (
                  <option key={p} value={p}>{p.charAt(0).toUpperCase()+p.slice(1)}</option>
                ))}
              </select>
            </div>
          </>
        )}

        {step === 2 && (
          <>
            <Input
              name="adminUsername"
              placeholder="Admin Username"
              value={form.adminUsername}
              onChange={handleChange}
              required
            />
            <Input
              name="adminEmail"
              type="email"
              placeholder="Admin Email"
              value={form.adminEmail}
              onChange={handleChange}
              required
            />
            <Input
              name="adminPassword"
              type="password"
              placeholder="Password"
              value={form.adminPassword}
              onChange={handleChange}
              required
            />
            <Input
              name="adminPassword2"
              type="password"
              placeholder="Confirm Password"
              value={form.adminPassword2}
              onChange={handleChange}
              required
            />
          </>
        )}

        <div className="flex justify-between mt-6">
          {step === 2 && (
            <Button
              type="button"
              variant="outline"
              onClick={handleBack}
              disabled={loading}
            >
              Back
            </Button>
          )}
          <Button
            type={step === 1 ? 'button' : 'submit'}
            onClick={step === 1 ? handleNext : undefined}
            disabled={loading}
          >
            {step === 1
              ? 'Next'
              : loading
              ? 'Creating…'
              : 'Create Account & Company'}
          </Button>
        </div>
      </form>
    </main>
  )
}
