import { EnvironmentProviders, makeEnvironmentProviders } from '@angular/core';
import { provideHttpClient, withFetch } from '@angular/common/http';

import { API_BASE_URL } from './api-base-url';

/** Registers HttpClient and the API base URL for every @12l/api service. */
export function provideApi(baseUrl: string): EnvironmentProviders {
  return makeEnvironmentProviders([provideHttpClient(withFetch()), { provide: API_BASE_URL, useValue: baseUrl }]);
}
